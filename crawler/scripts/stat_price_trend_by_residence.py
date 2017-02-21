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

#獲取需要監控的樓盤
def get_residences():
    return set([u'裕華大廈', u'保利達花園', u'亨達大廈', u'鴻發花園', u'綠楊花園', u'金海山花園'])
    #return set([u'亨達大廈'])

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

def init_data():
    residences_list = get_residences()
    ret = {}
    for residence in residences_list:
        ret[residence] = defaultdict(dict)
    return ret

def init_data_list():
    residences_list = get_residences()
    ret = {}
    for residence in residences_list:
        ret[residence] = defaultdict(list)
    return ret

def calc_condition(residence_info):
    if 'building' not in residence_info:
        return False
    if residence_info['building'] not in CALC_RESIDENCES:
        return False
    else: return True

def update_all_price_trend():
    date_beg = datetime.strptime('2016-01', '%Y-%m')
    print date_beg
    result = COLLECTION.find({'update_time':{'$gte':date_beg}})
    all_result = init_data()
    all_result_total = defaultdict(dict)

    all_price = init_data_list()
    all_price_total = defaultdict(list)

    all_price_list = []
    i = 0
    for res in result:
        #print res['price_history']
        if calc_condition(res['info']) == False:
            continue
        
        building = res['info']['building']
        price_his_items = sorted(res['price_history'].items())
        price_history = []
        for item in price_his_items:
            price_history.insert(0, item)
            #print price_history
            date = item[0][0:7]
            
            #print date
            r = calc_price_trend(price_history)
            
            all_result[building][date][str(res['_id'])] = r
            all_result_total[date][str(res['_id'])] = r
            #汇总价格
            price = item[1]
            if 'size' not in res['info'] or res['info']['size'] == 0:
                continue
            price_per_ft = (price * 10000) / res['info']['size']
            if price_per_ft > 1000000:
                print price, res['info']['size']
                print price_per_ft
                continue
            elif price_per_ft < 1000:
                print res['_id'], price, res['info']['size']
                print price_per_ft
                continue 

            all_price[building][date].append(price_per_ft)
            all_price_total[date].append(price_per_ft)
            all_price_list.append(price_per_ft)

        i += 1
        #if i >5:
            #break
    #计算呎价均值和标准差
    np_all_price = np.array(all_price_list)
    mean = np_all_price.mean()
    std = np_all_price.std()
    price_min = mean - std * 3
    price_max = mean + std * 3

    print mean, std, price_min, price_max
    #print all_result
    total_item = {}
    for cond in all_result:
        item = {'building':cond}
        for date in all_result[cond]:
            item[date] = {}
            item[date]['data'] = all_result[cond][date]
            item[date]['up'] = len(filter(lambda x:x[1] == 1, item[date]['data'].items()))
            item[date]['down'] = len(filter(lambda x:x[1] == -1, item[date]['data'].items()))
            item[date]['unchange'] = len(filter(lambda x:x[1] == 0, item[date]['data'].items()))
            item[date]['new'] = len(filter(lambda x:x[1] == 2, item[date]['data'].items()))
            item[date]['total'] = len(item[date]['data'])
            
            item[date]['update_time'] = datetime.now()

            #计算均价
            np_all_price = np.array(all_price[cond][date])
            np_all_price = np_all_price[(np_all_price>=price_min) & (np_all_price<=price_max)]
            #print np_all_price
            #print np_all_price[(np_all_price>=price_min) & (np_all_price<=price_max)]
            #print date
            if len(np_all_price) != 0:
                item[date]['avg'] = np_all_price.mean()
            #print item
            #del item['data']
        COLLECTION_RESIDENCE_PRICE_TREND_BY_RESIDENCE.update({'building':cond}, item, upsert = True)
        
    #json.dump(dict(all_result), open('test.json', 'w'), indent = 4, ensure_ascii = False)
    return

def update_all_price_trend_by_month(process_date):
    date_beg_str = process_date
    date_beg = datetime.strptime(date_beg_str, '%Y-%m')
    #print date_beg
    result = COLLECTION.find({'update_time':{'$gte':date_beg}})
    
    all_result = init_data()
    all_result_total = defaultdict(dict)

    all_price = init_data_list()
    all_price_total = defaultdict(list)

    all_price_list = []
    i = 0
    for res in result:
        #print res['price_history']
        if calc_condition(res['info']) == False:
            continue
        building = res['info']['building']
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
            all_result[building][date][str(res['_id'])] = r
            all_result_total[date][str(res['_id'])] = r
            #汇总价格
            price = item[1]
            if 'size' not in res['info'] or res['info']['size'] == 0:
                continue
            price_per_ft = (price * 10000) / res['info']['size']
            if price_per_ft > 1000000:
                print price, res['info']['size']
                print price_per_ft
                continue
            elif price_per_ft < 1000:
                print res['_id'], price, res['info']['size']
                print price_per_ft
                continue 

            all_price[building][date].append(price_per_ft)
            all_price_total[date].append(price_per_ft)
            all_price_list.append(price_per_ft)
        i += 1
        #if i >5:
            #break
    
    #计算呎价均值和标准差
    np_all_price = np.array(all_price_list)
    mean = np_all_price.mean()
    std = np_all_price.std()
    price_min = mean - std * 3
    price_max = mean + std * 3

    print mean, std, price_min, price_max

    for cond in all_result:
        item = {'building':cond}
        item[date_beg_str] = {}
        item[date_beg_str]['data'] = all_result[cond][date_beg_str]
        item[date_beg_str]['up'] = len(filter(lambda x:x[1] == 1, item[date_beg_str]['data'].items()))
        item[date_beg_str]['down'] = len(filter(lambda x:x[1] == -1, item[date_beg_str]['data'].items()))
        item[date_beg_str]['unchange'] = len(filter(lambda x:x[1] == 0, item[date_beg_str]['data'].items()))
        item[date_beg_str]['new'] = len(filter(lambda x:x[1] == 2, item[date_beg_str]['data'].items()))
        item[date_beg_str]['total'] = len(item[date_beg_str]['data'])
        
        item[date_beg_str]['update_time'] = datetime.now()
        #print item
        #del item['data']

        #计算均价
        np_all_price = np.array(all_price[cond][date_beg_str])
        #print np_all_price
        np_all_price = np_all_price[(np_all_price>=price_min) & (np_all_price<=price_max)]

        if len(np_all_price) != 0:
            item[date]['avg'] = np_all_price.mean()

        COLLECTION_RESIDENCE_PRICE_TREND_BY_RESIDENCE.update({'building':cond}, {'$set':item}, upsert = True)
        
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
COLLECTION_RESIDENCE_PRICE_TREND_BY_RESIDENCE = DB[settings['MONGODB_COLLECTION_PRICE_TREND_BY_RESIDENCE']]


DAYS_BEFORE = 30

CALC_RESIDENCES = get_residences()


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

    
