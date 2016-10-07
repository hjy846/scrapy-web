# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import logging
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from datetime import datetime
from scrapy.pipelines.images import ImagesPipeline
from malimalihome.items import MalimalihomeItem, ResidenceDetailItem, ResidenceImageItem


class MalimalihomePipeline(object):
    def __init__(self):
        self.server = settings['MONGODB_SERVER']
        self.port = settings['MONGODB_PORT']
        self.db = settings['MONGODB_DB_RAW']
        #self.col = settings['MONGODB_COLLECTION_RESIDENCE_BY_DAY']
        connection = pymongo.MongoClient(self.server, self.port)
        self.db = connection[self.db]   
        if settings.get('crawl_date', None):   
            #print 'why ' * 100 
            self.collection = self.db[settings['crawl_date']]
        else: self.collection = None

        self.image_collection = self.db[settings['MONGODB_COLLECTION_IMAGE']]

    def process_image(self, item):
        try:
            for image_info in item['images']:
                self.image_collection.update_one({'url':image_info['url']}, {'$set':dict(image_info)}, upsert = True)
        except Exception as e:
            #print '#' * 100
            logging.error(repr(e))
            print e
        #log.msg('ok', level = log.DEBUG, spider=spider)
        return item
        
    def process_detail(self, item):
        try:
            item['_id'] = int(item['_id'])
            self.collection.update_one({'_id':item['_id']}, {'$set':dict(item)}, upsert = True)
        except Exception as e:
            #print '#' * 100
            logging.error(repr(e))
            print e
        #log.msg('ok', level = log.DEBUG, spider=spider)
        return item

    def process_item(self, item, spider):
        if isinstance(item, ResidenceImageItem):
            return self.process_image(item)
        elif isinstance(item, ResidenceDetailItem) or isinstance(item, MalimalihomeItem):
            return self.process_detail(item)
        else:
            raise DropItem('unknown item')


class MyImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item