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
import numpy as np


reload(sys)
sys.setdefaultencoding('utf-8')

def get_param(sys):
    #处理时间
    if len(sys.argv) >= 2:
        crawl_date = sys.argv[1]
    else: crawl_date = 'yesterday'

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
        crawl_date = crawl_date if crawl_date else yesterday_str

    #settings['crawl_date'] = self.crawl_date
    return {'crawl_date':crawl_date}

def stat_dsf(month = '', dsf_type = 'xianlou'):
    collection = None
    if dsf_type == 'xianlou':
        collection = COLLECTION_DSF_XIANLOU
    elif dsf_type == 'louhua':
        collection = COLLECTION_DSF_LOUHUA
    else:
        dsf_type = 'total'
        collection = COLLECTION_DSF

    if month == '':
        result = collection.find().sort('date', pymongo.DESCENDING).limit(1)
    elif month == 'all':
        result = collection.find()

    print dsf_type
    for res in result:
        item = {}
        age = defaultdict(int)
        region = defaultdict(int)
        region_price = {}
        region_size = {}
        price = defaultdict(int)
        for detail in res['detail_stat']:
            if detail['age'] == 'all':
                if detail['height'] == 'all' and detail['index'] != 'all':
                    region_price[detail['region']] = int(detail['avage_price'] / 10000)
                    region_size[detail['region']] = detail['size']
                    region[detail['region']] = detail['volumn']
                    print detail
                else:
                    continue
            else:
                age[detail['age']] += detail['volumn']
                #region[detail['region']] += detail['volumn']
                price[str(detail['avage_price'] / 10000)] += detail['volumn']
        
        item['date'] = res['date']
        #按樓齡統計成交數
        item['age'] = age
        #按地區統計成交數
        item['region'] = region
        #按地區統計成交價格
        item['region_price'] = region_price
        #按地區統計平均成交面積
        item['region_size'] = region_size
        #按價格統計成交數
        item['price'] = price

        item['dsf_type'] = dsf_type
        #print item
        COLLECTION_DSF_STAT.update({'date':res['date'], 'dsf_type':dsf_type}, item, upsert = True)

def stat_dsf_all():
    #統計所有日期
    month = 'all'
    dsf_type = 'xianlou'
    stat_dsf(month, dsf_type)

    dsf_type = 'louhua'
    stat_dsf(month, dsf_type)

    dsf_type = 'total'
    stat_dsf(month, dsf_type)

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
COLLECTION_RESIDENCE_PRICE_TREND = DB[settings['MONGODB_COLLECTION_PRICE_TREND']]
COLLECTION_RESIDENCE_PRICE_TREND_MONTH = DB[settings['MONGODB_COLLECTION_PRICE_TREND_MONTH']]

COLLECTION_DSF = DB[settings['MONGODB_COLLECTION_DSF_RAW']]
COLLECTION_DSF_LOUHUA = DB[settings['MONGODB_COLLECTION_DSF_LOUHUA_RAW']]
COLLECTION_DSF_XIANLOU = DB[settings['MONGODB_COLLECTION_DSF_XIANLOU_RAW']]
COLLECTION_DSF_STAT = DB[settings['MONGODB_COLLECTION_DSF_STAT']]
DAYS_BEFORE = 30

if __name__ == '__main__':
    print PARAMS['crawl_date']
    process_date = datetime.strptime(PARAMS['crawl_date'], '%Y-%m-%d') - timedelta(1)
    
    process_date = process_date.strftime('%Y-%m')
    print process_date
    
    #stat_dsf()
    stat_dsf_all()
    

    
