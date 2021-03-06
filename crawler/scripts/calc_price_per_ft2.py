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

def stat_price(query_dict):
    result = COLLECTION.find({'info.price_per_ft2':{'$exists':False}})
    
    for res in result:
        try:
            price_per_ft2 = 0
            if 'size' in res['info']:
                #print res['info']['price'] , res['info']['size']
                price_per_ft2 = res['info']['price'] * 10000 / res['info']['size']
                print price_per_ft2
            print 'id'
            print res['_id']
            COLLECTION.update({'_id':res['_id']}, {'$set':{'info.price_per_ft2':price_per_ft2}})
            
        except Exception as e:
            print res['info']

if __name__ == '__main__':
    print PARAMS['crawl_date']
    date_beg = "2016-08-01"
    date_end = "2016-08-31"
    stat_price({"info.update_time":{"$gt":date_beg, "$lt":date_end}, "info.region":u"氹仔"})

    