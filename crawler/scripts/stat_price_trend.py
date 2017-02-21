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

'''
跟上一次价格变化数据比
'''
def calc_price_trend1(price_history):
    ret = 0
    
    #print price_his_items
    price_change = []
    cur_price = -1
    cur_date = ''
    for item in price_history:
        if item[1] != cur_price:
            cur_price = item[1]
            cur_date = item[0]
            price_change.append((item[0], item[1]))
    if len(price_change) > 1:
        print price_history
        print price_change
        if price_change[0][1] > price_change[1][1]:
            ret = 1
        elif price_change[0][1] < price_change[1][1]:
            ret = -1
        print ret
    return ret
'''
跟上一次报价比
'''
def calc_price_trend(price_history):
    ret = 0
    
    if len(price_history) > 1:
        if price_history[0][1] > price_history[1][1]:
            ret = 1
        elif price_history[0][1] < price_history[1][1]:
            ret = -1
    elif len(price_history) == 1:
        ret = 2 #新盘
    #if ret != 0:
        #print price_history
    return ret

def update_price_trend():
    date_beg = datetime.strptime('2017-02-14', '%Y-%m-%d')
    print date_beg
    result = COLLECTION.find({'update_time':{'$gte':date_beg}})
    for res in result:
        #print res['price_history']
        price_his_items = sorted(res['price_history'].items(),  reverse = True)
        r = calc_price_trend(price_his_items)
    return

def update_all_price_trend():
    date_beg = datetime.strptime('2016-02', '%Y-%m')
    print date_beg
    result = COLLECTION.find({'update_time':{'$gte':date_beg}})
    all_result = defaultdict(dict)
    all_result_macau = defaultdict(dict)
    all_result_taipa = defaultdict(dict)
    all_result_coloane = defaultdict(dict)
    i = 0
    for res in result:
        #print res['price_history']
        price_his_items = sorted(res['price_history'].items())
        price_history = []
        for item in price_his_items:
            price_history.insert(0, item)
            #print price_history
            date = item[0][0:7]
            #print date
            r = calc_price_trend(price_history)
            all_result[date][str(res['_id'])] = r
            if 'region' not in res['info']:
                continue
            if res['info']['region'] == u'澳門':
                all_result_macau[date][str(res['_id'])] = r
            elif res['info']['region'] == u'氹仔':
                all_result_taipa[date][str(res['_id'])] = r
            elif res['info']['region'] == u'路環':
                all_result_coloane[date][str(res['_id'])] = r

        i += 1
        #if i >5:
            #break
    
    for key in all_result:
        item = {}
        item['date'] = key
        item['data'] = all_result[key]
        item['data_macau'] = all_result_macau[key]
        item['data_taipa'] = all_result_taipa[key]
        item['data_coloane'] = all_result_coloane[key]
        item['up'] = len(filter(lambda x:x[1] == 1, item['data'].items()))
        item['down'] = len(filter(lambda x:x[1] == -1, item['data'].items()))
        item['unchange'] = len(filter(lambda x:x[1] == 0, item['data'].items()))
        item['new'] = len(filter(lambda x:x[1] == 2, item['data'].items()))
        item['total'] = len(item['data'])
        item['up_macau'] = len(filter(lambda x:x[1] == 1, item['data_macau'].items()))
        item['down_macau'] = len(filter(lambda x:x[1] == -1, item['data_macau'].items()))
        item['unchange_macau'] = len(filter(lambda x:x[1] == 0, item['data_macau'].items()))
        item['new_macau'] = len(filter(lambda x:x[1] == 2, item['data_macau'].items()))
        item['total_macau'] = len(item['data_macau'])
        item['up_taipa'] = len(filter(lambda x:x[1] == 1, item['data_taipa'].items()))
        item['down_taipa'] = len(filter(lambda x:x[1] == -1, item['data_taipa'].items()))
        item['unchange_taipa'] = len(filter(lambda x:x[1] == 0, item['data_taipa'].items()))
        item['new_taipa'] = len(filter(lambda x:x[1] == 2, item['data_taipa'].items()))
        item['total_taipa'] = len(item['data_taipa'])
        item['up_coloane'] = len(filter(lambda x:x[1] == 1, item['data_coloane'].items()))
        item['down_coloane'] = len(filter(lambda x:x[1] == -1, item['data_coloane'].items()))
        item['unchange_coloane'] = len(filter(lambda x:x[1] == 0, item['data_coloane'].items()))
        item['new_coloane'] = len(filter(lambda x:x[1] == 2, item['data_coloane'].items()))
        item['total_coloane'] = len(item['data_coloane'])
        item['update_time'] = datetime.now()

        #print item
        #del item['data']
        COLLECTION_RESIDENCE_PRICE_TREND_MONTH.update({'date':key}, item, upsert = True)
        
    #json.dump(dict(all_result), open('test.json', 'w'), indent = 4, ensure_ascii = False)
    return

def update_all_price_trend_by_month(process_date):
    date_beg_str = process_date
    date_beg = datetime.strptime(date_beg_str, '%Y-%m')

    #print date_beg
    result = COLLECTION.find({'update_time':{'$gte':date_beg}})
    
    all_result = defaultdict(dict)
    all_result_macau = defaultdict(dict)
    all_result_taipa = defaultdict(dict)
    all_result_coloane = defaultdict(dict)
    i = 0
    for res in result:
        #print res['price_history']
        price_his_items = sorted(res['price_history'].items())
        price_history = []
        for item in price_his_items:
            price_history.insert(0, item)
            #print price_history
            date = item[0][0:7]
            if date != date_beg_str:
                continue
            #print date
            r = calc_price_trend(price_history)
            all_result[str(res['_id'])] = r
            if 'region' not in res['info']:
                continue
            if res['info']['region'] == u'澳門':
                all_result_macau[date][str(res['_id'])] = r
            elif res['info']['region'] == u'氹仔':
                all_result_taipa[date][str(res['_id'])] = r
            elif res['info']['region'] == u'路環':
                all_result_coloane[date][str(res['_id'])] = r
        i += 1
        #if i >5:
            #break
    
    item = {}
    item['date'] = date_beg_str
    item['data'] = all_result
    item['data_macau'] = all_result_macau[item['date']]
    item['data_taipa'] = all_result_taipa[item['date']]
    item['data_coloane'] = all_result_coloane[item['date']]
    item['up'] = len(filter(lambda x:x[1] == 1, item['data'].items()))
    item['down'] = len(filter(lambda x:x[1] == -1, item['data'].items()))
    item['unchange'] = len(filter(lambda x:x[1] == 0, item['data'].items()))
    item['new'] = len(filter(lambda x:x[1] == 2, item['data'].items()))
    item['total'] = len(item['data'])
    item['up_macau'] = len(filter(lambda x:x[1] == 1, item['data_macau'].items()))
    item['down_macau'] = len(filter(lambda x:x[1] == -1, item['data_macau'].items()))
    item['unchange_macau'] = len(filter(lambda x:x[1] == 0, item['data_macau'].items()))
    item['new_macau'] = len(filter(lambda x:x[1] == 2, item['data_macau'].items()))
    item['total_macau'] = len(item['data_macau'])
    item['up_taipa'] = len(filter(lambda x:x[1] == 1, item['data_taipa'].items()))
    item['down_taipa'] = len(filter(lambda x:x[1] == -1, item['data_taipa'].items()))
    item['unchange_taipa'] = len(filter(lambda x:x[1] == 0, item['data_taipa'].items()))
    item['new_taipa'] = len(filter(lambda x:x[1] == 2, item['data_taipa'].items()))
    item['total_taipa'] = len(item['data_taipa'])
    item['up_coloane'] = len(filter(lambda x:x[1] == 1, item['data_coloane'].items()))
    item['down_coloane'] = len(filter(lambda x:x[1] == -1, item['data_coloane'].items()))
    item['unchange_coloane'] = len(filter(lambda x:x[1] == 0, item['data_coloane'].items()))
    item['new_coloane'] = len(filter(lambda x:x[1] == 2, item['data_coloane'].items()))
    item['total_coloane'] = len(item['data_coloane'])
    item['update_time'] = datetime.now()
    #print item
    #del item['data']
    COLLECTION_RESIDENCE_PRICE_TREND_MONTH.update({'date':date_beg_str}, item, upsert = True)
        
    #json.dump(dict(all_result), open('test.json', 'w'), indent = 4, ensure_ascii = False)
    return

def calc_date():
    result = COLLECTION.find()
    count = 0
    for res in result:
        if '2016-05-18' in res['price_history']:
            count += 1
    print count

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


DAYS_BEFORE = 30

if __name__ == '__main__':
    print PARAMS['crawl_date']
    process_date = datetime.strptime(PARAMS['crawl_date'], '%Y-%m-%d') - timedelta(1)
    
    process_date = process_date.strftime('%Y-%m')
    print process_date
    update_all_price_trend_by_month(process_date)
    #update_all_price_trend()
    #calc_date()
    #find_new_residences()
    #stat_region_data()

    
