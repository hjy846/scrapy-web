# -*- coding: utf-8 -*-
import scrapy
import sys
import time
import urlparse
import os
from datetime import datetime, timedelta
import json
from scrapy.conf import settings
import pymongo
import logging
from scrapy.conf import settings
from crawler.items import ResidenceItem, ResidenceDetailItem, ResidenceImageItem

reload(sys)
sys.setdefaultencoding('utf-8')

class ResidenceImageSpider(scrapy.Spider):
    name = "residence_image"
    #allowed_domains = ["xxx.net"]
    start_urls = []
    start_urls.append(settings['START_URL'])


    def __init__(self, crawl_date = None, region = None, *args, **kwargs):
        super(ResidenceImageSpider, self).__init__(*args, **kwargs)
        #处理时间
        now = datetime.now()
        yesterday = now - timedelta(days=1)
        yesterday_str = yesterday.strftime('%Y-%m-%d')

        today_str = now.strftime('%Y-%m-%d')

        if crawl_date == 'today':
            self.crawl_date = today_str
        elif crawl_date == 'yesterday':
            self.crawl_date = yesterday_str
        else:
            self.crawl_date = crawl_date if crawl_date else yesterday_str
        #help(settings)
        settings.set('crawl_date', self.crawl_date)
        #settings['crawl_date'] = self.crawl_date
        self.now = now.strftime('%Y%m%d_%H%M')

        

    def load_image_url(self):
        self.server = settings['MONGODB_SERVER']
        self.port = settings['MONGODB_PORT']
        self.db = settings['MONGODB_DB_RAW']
        connection = pymongo.MongoClient(self.server, self.port)
        self.db = connection[self.db]   
        if settings.get('crawl_date', None):   
            self.collection = self.db[settings['crawl_date']]
        else: self.collection = None
        res = self.collection.find()
        for r in res:
            item = ResidenceImageItem()
            item['image_urls'] = r['image_list']
            yield item


    def parse(self, response):
        image_list = self.load_image_url()
        for image_item in image_list:
            yield image_item

