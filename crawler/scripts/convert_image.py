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
IMAGE_COLLECTION = RAW_DB[settings['MONGODB_COLLECTION_IMAGE']]

COLLECTION = DB[settings['MONGODB_COLLECTION_ALL_RESIDENCES']]

if __name__ == '__main__':
    time = datetime.strptime(PARAMS['crawl_date'], '%Y-%m-%d')
    residence_image_dict = {}
    for r in COLLECTION.find({'update_time':{'$gt':time}}):
        try:
            image_list_new = []
            
            for image_url in r['info']['image_list']:
                img_info = IMAGE_COLLECTION.find_one({'url':image_url})
                if img_info == None:
                    image_list_new.append(image_url)
                else:
                    url = '/static/residence_images/%s' % img_info.get('path', '')
                    image_list_new.append(url)
            residence_image_dict[r['_id']] = image_list_new
        except Exception as e:
            print r
            print e

    json.dump(residence_image_dict, open('residence_image.json', 'w'), indent = 4, ensure_ascii = False)

    print 'begin update'
    for i in residence_image_dict:
        COLLECTION.update({'_id':i}, {'$set':{'image_list_new':residence_image_dict[i]}}, upsert = True)

