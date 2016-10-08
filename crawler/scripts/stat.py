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
    find_param = {'region':u"氹仔"}
    print find_param
    count = RAW_COLLECTION.count(find_param)
    result = {}
    result['taipa'] = count

    find_param = {'region':u"澳門"}
    print find_param
    count = RAW_COLLECTION.count(find_param)
    result['macau'] = count

    find_param = {'region':u"路環"}
    print find_param
    count = RAW_COLLECTION.count(find_param)
    result['coloane'] = count
    result['date'] = PARAMS['crawl_date']
    COLLECTION_RESIDENCE_NUM_BY_DAY.update({'date': PARAMS['crawl_date']}, result, upsert = True)

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
    stat_region_data()

    