# -*- coding: utf-8 -*-
import sys
import time
import urlparse
import os
from datetime import datetime, timedelta
import json
import pymongo
import logging
from scrapy.conf import settings
from collections import defaultdict


reload(sys)
sys.setdefaultencoding('utf-8')

def get_param(sys):
    #处理时间
    if len(sys.argv) >= 2:
        crawl_date = sys.argv[1]
    else: crawl_date = 'today'

    now = datetime.now()
    yesterday = now - timedelta(days=1)
    now = datetime.now()
    yesterday_str = yesterday.strftime('%Y-%m-%d')
    today_str = now.strftime('%Y-%m-%d')
    if crawl_date == 'today':
        crawl_date = today_str
    elif crawl_date == 'yesterday':
        crawl_date = yesterday_str
    else:
        crawl_date = crawl_date if crawl_date else today_str

    #settings['crawl_date'] = self.crawl_date
    return {'crawl_date':crawl_date}

def insert_into_all_residences():
    server = settings['MONGODB_SERVER']
    port = settings['MONGODB_PORT']
    raw_db = settings['MONGODB_DB_RAW']
    connection = pymongo.MongoClient(server, port)
    raw_db = connection[raw_db]   
    raw_collection = raw_db[PARAMS['crawl_date']]
    res = raw_collection.find()
    
    image_collection = raw_db[settings['MONGODB_COLLECTION_IMAGE']]

def find_new_residences():
    COLLECTION_NEW_ADD.remove({'date':PARAMS['crawl_date']})
    res = RAW_COLLECTION.find()
    for r in res:
        _id = r['_id']
        #替换image url

        save_record = {'info':r, 'update_time':datetime.now(), 'price_history.%s' % r['update_time']:r['price']}
        if COLLECTION.find_one({'_id':_id}) == None:
            r['create_time'] = datetime.now()
            save_record['create_time'] = datetime.now()
            try:
                COLLECTION_NEW_ADD.update({'date':PARAMS['crawl_date']}, {"$push":{r['region']:r, 'total':r}}, upsert = True)
                #print 'new add'
            except Exception as e:
                print e

        COLLECTION.update({'_id':_id}, {'$set':save_record}, upsert = True)

def stat_region_data():
    find_param = {'region':u"氹仔"}
    count = RAW_COLLECTION.count(find_param)
    result = {}
    result['taipa'] = count

    find_param = {'region':u"澳門"}
    count = RAW_COLLECTION.count(find_param)
    result['macau'] = count

    find_param = {'region':u"路環"}
    count = RAW_COLLECTION.count(find_param)
    result['coloane'] = count

    count = RAW_COLLECTION.count()
    result['total'] = count
    result['date'] = PARAMS['crawl_date']
    result['insert_time'] = datetime.now()

    new_add = COLLECTION_NEW_ADD.find_one({'date':PARAMS['crawl_date']})
    #print result
    #print new_add.keys()
    if new_add:
        result['taipa_new'] = len(new_add.get(u'氹仔', []))
        result['macau_new'] = len(new_add.get(u'澳門', []))
        result['coloane_new'] = len(new_add.get(u'路環', []))
        result['total_new'] = len(new_add.get('total', []))
    #print result
    COLLECTION_RESIDENCE_NUM_BY_DAY.update({'date': PARAMS['crawl_date']}, result, upsert = True)

def insert_into_raw(data):
    RAW_COLLECTION.update_one({'_id':data['_id']}, {'$set':data}, upsert = True)

PARAMS = get_param(sys)

SERVER = settings['MONGODB_SERVER']
PORT = settings['MONGODB_PORT']
DB = settings['MONGODB_DB']
RAW_DB = settings['MONGODB_DB_RAW']
CONNECTION = pymongo.MongoClient(SERVER, PORT)
RAW_DB = CONNECTION[RAW_DB] 
DB = CONNECTION[DB]  
RAW_COLLECTION = RAW_DB[PARAMS['crawl_date']]
IMAGE_COLLECTION = RAW_DB[settings['MONGODB_COLLECTION_IMAGE']]

COLLECTION = DB[settings['MONGODB_COLLECTION_ALL_RESIDENCES']]
COLLECTION_NEW_ADD = DB[settings['MONGODB_COLLECTION_NEW_ADD']]
COLLECTION_RESIDENCE_NUM_BY_DAY = DB[settings['MONGODB_COLLECTION_RESIDENCE_NUM_BY_DAY']]

if __name__ == '__main__':
    ubuntu_data = defaultdict(list)
    for i in os.walk('D:\code\scrapy-web\malimalihome\ubuntu_output'):
        if 'items.txt' in i[2]:
            items = i[0].split('\\')
            #print items
            region = items[-2]
            if region == 'taipa':
                region = u'氹仔'
            elif region == 'macau':
                region = u'澳門'
            elif region == 'coloane':
                region = u'路環'
            else:
                print 'error'
                print region
                exit()
            date = items[-3].split('_')[0]
            #date = '%s-%s-%s' % (date[0:4], date[4:6],date[6:8])
            path = os.path.join(i[0], 'items.txt')
            #print region, date, path
            with open(path) as fp:
                for line in fp:
                    data = json.loads(line)
                    data['_id'] = int(data['link'].strip().split('/')[-1])
                    data['region'] = region
                    data['building'] = data['building_name'].strip().split()[0]
                    data['list_insert_time'] = datetime.now()
                    ubuntu_data[date].append(data)
    #print len(ubuntu_data['2016-05-11'])
    date_sorted = sorted(ubuntu_data.keys())
    for date in date_sorted:
        PARAMS['crawl_date'] = date
        RAW_COLLECTION = RAW_DB[date]
        print PARAMS['crawl_date']
        #print len(ubuntu_data[date])
        for data in ubuntu_data[date]:
            #print data
            insert_into_raw(data)
        find_new_residences()
        stat_region_data()
        #break

    #find_new_residences()
    #stat_region_data()

    