#! -*- coding: utf-8 -*-
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

def stat_region_data():
    return 

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
    result = COLLECTION.find()
    for r in result:
        first_release_time = sorted(r['price_history'].keys())[0]
        COLLECTION.update({'_id':r['_id']}, {'$set':{'first_release_time':first_release_time}}, upsert = True)

    