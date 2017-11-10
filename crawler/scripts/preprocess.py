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
from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors
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

def update_residences():
    sql_raw = "select * from residence_raw_hour where crawl_date = '%s';" % PARAMS['crawl_date']
    cursor.execute(sql_raw)
    res = cursor.fetchall()
    for r in res:
        bid = r['bid']
        price_history = {r['crawl_date']:r['price']}
        #插入数据
        sql_upsert = "insert into all_residences(create_time, bid, living_room_num, rent, property_type, photo_num, size, layout, \
                    floor, rental_per_ft2, direction, other, location, building_name, update_time, agent_logo, views, price, lift, \
                    link, rental, renovation, building, remark, price_per_ft2, room, region, net_size, detail_insert_time, \
                    bed_room_num, list_insert_time, age, block, first_release_time, agent_name, agent_contact, agent_company,\
                    agent_address, image_list, price_history) \
                VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', \
                    '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', \
                    '%s', '%s', '%s', '%s', '%s', '%s') \
                ON DUPLICATE KEY UPDATE living_room_num = '%s', rent = '%s', property_type = '%s', photo_num = '%s', \
                    size = '%s', layout = '%s', floor = '%s', rental_per_ft2 = '%s', direction = '%s', other = '%s', \
                    location = '%s', building_name = '%s', update_time = '%s', agent_logo = '%s', views = '%s', price = '%s', lift = '%s', \
                    link = '%s', rental = '%s', renovation = '%s', building = '%s', remark = '%s', price_per_ft2 = '%s', \
                    room = '%s', region = '%s', net_size = '%s', detail_insert_time = '%s', bed_room_num = '%s', \
                    list_insert_time = '%s', age = '%s', block = '%s', agent_name = '%s', agent_contact = '%s', \
                    agent_company = '%s', agent_address = '%s', image_list = '%s', price_history = JSON_SET(price_history, '$.\"%s\"', %s);" % \
                (datetime.now(), r['bid'], r['living_room_num'], r['rent'], r['property_type'], r['photo_num'], r['size'], r['layout'], \
                    r['floor'], r['rental_per_ft2'], r['direction'], r['other'], r['location'], r['building_name'], r['crawl_date'], r['agent_logo'], \
                    r['views'], r['price'], r['lift'], r['link'], r['rental'], r['renovation'], r['building'], r['remark'], \
                    r['price_per_ft2'], r['room'], r['region'], r['net_size'], r['detail_insert_time'], r['bed_room_num'], \
                    r['list_insert_time'], r['age'], r['block'], r['crawl_date'], r['agent_name'], r['agent_contact'], \
                    r['agent_company'], r['agent_address'], r['image_list'], json.dumps(price_history), r['living_room_num'], r['rent'], r['property_type'], \
                    r['photo_num'], r['size'], r['layout'], r['floor'], r['rental_per_ft2'], r['direction'], r['other'], \
                    r['location'], r['building_name'], r['crawl_date'], r['agent_logo'], r['views'], r['price'], r['lift'], r['link'], \
                    r['rental'], r['renovation'], r['building'], r['remark'], r['price_per_ft2'], r['room'], r['region'], \
                    r['net_size'], r['detail_insert_time'], r['bed_room_num'], r['list_insert_time'], r['age'], r['block'], \
                    r['agent_name'], r['agent_contact'], r['agent_company'], r['agent_address'], r['image_list'], r['crawl_date'], r['price'])
        try:
            cursor.execute(sql_upsert)
            db.commit()
        except MySQLdb.Error, e:
            print(e)
    

def stat_region_data():
    sql = "select * from all_residences where update_time = '%s'" % PARAMS['crawl_date']
    cursor.execute(sql)
    res = cursor.fetchall()
    result = defaultdict(int)
    for r in res:
        result['total'] += 1
        if r['region'] == u"氹仔":
            result['taipa'] += 1
        elif r['region'] == u"澳門":
            result['macau'] += 1
        elif r['region'] == u"路環":
            result['coloane'] += 1
        else: result['other'] += 1

        if r['first_release_time'] == r['update_time']:
            result['total_new'] += 1
            if r['region'] == u"氹仔":
                result['taipa_new'] += 1
            elif r['region'] == u"澳門":
                result['macau_new'] += 1
            elif r['region'] == u"路環":
                result['coloane_new'] += 1
            else: result['other_new'] += 1


    sql_upsert = "insert into residence_num_by_day (date, total, macau, taipa, coloane, other, total_new, macau_new, \
                    taipa_new, coloane_new, other_new, create_time) \
                VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s') \
                ON DUPLICATE KEY UPDATE total = '%s', macau = '%s', taipa = '%s', coloane = '%s', other = '%s', total_new = '%s', \
                    macau_new = '%s', taipa_new = '%s', coloane_new = '%s', other_new = '%s'" \
                % (PARAMS['crawl_date'], result['total'], result['macau'], result['taipa'], result['coloane'], result['other'], \
                    result['total_new'], result['macau_new'], result['taipa_new'], result['coloane_new'], result['other_new'], \
                    datetime.now(), result['total'], result['macau'], result['taipa'], result['coloane'], result['other'], \
                    result['total_new'], result['macau_new'], result['taipa_new'], result['coloane_new'], result['other_new'])
    cursor.execute(sql_upsert)
    db.commit()
    

PARAMS = get_param(sys)

#SERVER = settings['MONGODB_SERVER']
#PORT = settings['MONGODB_PORT']
#DB = settings['MONGODB_DB']
#RAW_DB = settings['MONGODB_DB_RAW']
#CONNECTION = pymongo.MongoClient(SERVER, PORT)
#RAW_DB = CONNECTION[RAW_DB] 
#DB = CONNECTION[DB]  
#RAW_COLLECTION = RAW_DB[PARAMS['crawl_date']]
#IMAGE_COLLECTION = RAW_DB[settings['MONGODB_COLLECTION_IMAGE']]

#COLLECTION = DB[settings['MONGODB_COLLECTION_ALL_RESIDENCES']]
#COLLECTION_NEW_ADD = DB[settings['MONGODB_COLLECTION_NEW_ADD']]
#COLLECTION_RESIDENCE_NUM_BY_DAY = DB[settings['MONGODB_COLLECTION_RESIDENCE_NUM_BY_DAY']]
dbargs = dict(
            host = '127.0.0.1' ,
            db = 'property',
            user = 'root', #replace with you user name
            passwd = '', # replace with you password
            charset = 'utf8',
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode = True,
            )    

#dbpool = adbapi.ConnectionPool('MySQLdb',**dbargs)
db = MySQLdb.connect("localhost","root","","property", use_unicode = True, charset = "utf8")
cursor = db.cursor(MySQLdb.cursors.DictCursor)


if __name__ == '__main__':
    print PARAMS['crawl_date']
    #PARAMS['crawl_date'] = "2017-11-08"
    print "update residences"
    update_residences()
    print "stat residences by region"
    stat_region_data()

    
