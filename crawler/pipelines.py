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
from crawler.items import ResidenceItem, ResidenceDetailItem, ResidenceImageItem, ZhongyuanItem
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTFigure

from collections import defaultdict
import json

from datetime import datetime
import copy
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class ResidencePipeline(object):
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
                #print image_info['url']
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
        elif isinstance(item, ResidenceDetailItem) or isinstance(item, ResidenceItem):
            return self.process_detail(item)
        return item
        #else:
        #    raise DropItem('unknown item')


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

class ZhongyuanPipeline(object):
    def __init__(self):
        self.server = settings['MONGODB_SERVER']
        self.port = settings['MONGODB_PORT']
        self.db = settings['MONGODB_DB']
        #self.col = settings['MONGODB_COLLECTION_RESIDENCE_BY_DAY']
        connection = pymongo.MongoClient(self.server, self.port)
        self.db = connection[self.db]   
        self.collection = self.db[settings['MONGODB_COLLECTION_ZHONGYUAN']]
        
    def convert_pdf_2_text(self, path):

        rsrcmgr = PDFResourceManager()
        laparams = LAParams()

        device = PDFPageAggregator(rsrcmgr, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        fp = open(path, 'rb')
        parser = PDFParser(fp)
        document = PDFDocument(parser)

        
        layout_list = []

        for page in PDFPage.create_pages(document):
            interpreter.process_page(page)
            layout = device.get_result()
            layout_dict = defaultdict(list)
            for x in layout:
                try:

                    t = x.get_text().strip()
                    #help(x)
                    #exit()
                    #axis = "%s_%s" % (x.__dict__['x0'], x.__dict__['x1'])
                    axis = "%s" % (x.__dict__['y0'])
                    #print x
                    layout_dict[axis].append((x.__dict__['x0'], t))
                    #print x,t
                    
                except Exception as e:
                    pass
                    #print e
            
            new_layout_dict = defaultdict(list)
            for key in layout_dict:
                sorted_list = sorted(layout_dict[key], key = lambda x:x[0])
                #print 'sorted list'
                #print sorted_list
                new_layout_dict[key] = [x[1] for x in sorted_list]
                #print key, new_layout_dict[key]

            ll = sorted(new_layout_dict.items(), key = lambda x:-float(x[0]))
            layout_list.extend(ll)
        device.close()

        #print layout_dict
        return layout_list

    def process_pdf(self, item):
        residence_list = self.convert_pdf_2_text(item['path'])
        #residence_list = sorted(residence_dict.items(), key = lambda x:-float(x[0]))
        #json.dump(residence_list, open('result.json', 'w'), indent = 4, ensure_ascii = False)

        region = 'taipa'
        date_str = residence_list[0][1][0]
        date_list = date_str.strip().split('20')[1:]
        date_beg = date_list[0].strip('~').split('.')
        date_end = date_list[1].split('.')
        date_beg = '20%s-%s-%s' % (date_beg[0], date_beg[1], date_beg[2])
        date_end = '20%s-%s-%s' % (date_end[0], date_end[1], date_end[2])
        #print date_beg, date_end
        
        for info in residence_list[1:-1]:
            try:
                if len(info[1]) == 1:
                    if u'氹仔' in info[1][0]:
                        region = 'taipa'
                    elif u'澳門' in info[1][0]:
                        region = 'macau'
                    if u'租賃成交' in info[1][0]:
                        #print 'rent'
                        #print info
                        break
                    continue

                if u'樓宇名稱' in info[1][0]:
                    continue

                residence = {}
                residence['building'] = info[1][0]
                residence['block_floor'] = info[1][1]
                if len(info[1]) == 6:
                    residence['remark'] = ""
                    residence['size'] = int(''.join(info[1][2].split(',')))
                    residence['price'] = int(''.join(info[1][3].strip('$').split(','))) / 10000
                    residence['price_per_ft2'] = int(''.join(info[1][4].strip('$').split(',')))
                    residence['market'] = info[1][5]
                else:
                    if info[1][2] == '':
                        residence['remark'] = ""
                        residence['size'] = int(''.join(info[1][3].split(',')))
                        residence['price'] = int(''.join(info[1][4].strip('$').split(','))) / 10000
                        residence['price_per_ft2'] = int(''.join(info[1][5].strip('$').split(',')))
                        residence['market'] = info[1][6]
                    else:
                        residence['size'] = int(''.join(info[1][2].split(',')))
                        residence['price'] = int(''.join(info[1][3].strip('$').split(','))) / 10000
                        residence['price_per_ft2'] = int(''.join(info[1][4].strip('$').split(',')))
                        residence['remark'] = info[1][5]
                        residence['market'] = info[1][6]
                    
                residence['region'] = region
                residence['date_beg'] = date_beg
                residence['date_end'] = date_end
                find_residence = copy.deepcopy(residence)
                residence['insert_time'] = datetime.now()
                #print i
            
                self.collection.update(find_residence, {'$set':residence}, upsert = True)
            except Exception as e:
                print 'Error'
                print item['path']
                print info
                print e
                continue
            #print item
        return item

    def process_item(self, item, spider):
        #print '#@**' * 100
        #print item
        #print type(item)
        if isinstance(item, ZhongyuanItem):
            return self.process_pdf(item)
        else:
            return item