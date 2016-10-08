# -*- coding: utf-8 -*-

import os
import sys
from cStringIO import StringIO

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

sys.path.append('..')
from crawler import settings
import pymongo
from datetime import datetime
import copy

reload(sys)
sys.setdefaultencoding('utf-8')

def convert_pdf_2_text(path):

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

SERVER = settings.MONGODB_SERVER
PORT = settings.MONGODB_PORT
DB = settings.MONGODB_DB
COLLECTION_NAME = 'centaline'
CONNECTION = pymongo.MongoClient(SERVER, PORT)
DB = CONNECTION[DB]  
COLLECTION = DB[COLLECTION_NAME]

if __name__ == '__main__':

    path = './8.15.pdf'
    if len(sys.argv) >= 2:
        path = sys.argv[1]

    residence_list = convert_pdf_2_text(path)
    #residence_list = sorted(residence_dict.items(), key = lambda x:-float(x[0]))
    json.dump(residence_list, open('result.json', 'w'), indent = 4, ensure_ascii = False)

    region = 'taipa'
    date_str = residence_list[0][1][0]
    date_list = date_str.strip().split('20')[1:]
    date_beg = date_list[0].strip('~').split('.')
    date_end = date_list[1].split('.')
    date_beg = '20%s-%s-%s' % (date_beg[0], date_beg[1], date_beg[2])
    date_end = '20%s-%s-%s' % (date_end[0], date_end[1], date_end[2])
    print date_beg, date_end
    
    for info in residence_list[1:-1]:
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

        if info[1][0] == u'樓宇名稱':
            continue

        item = {}
        item['building'] = info[1][0]
        item['block_floor'] = info[1][1]
        item['remark'] = info[1][2]
        item['size'] = int(''.join(info[1][3].split(',')))
        item['price'] = int(''.join(info[1][4].strip('$').split(','))) / 10000
        item['price_per_ft2'] = int(''.join(info[1][5].strip('$').split(',')))
        item['market'] = info[1][6]
        item['region'] = region
        item['date_beg'] = date_beg
        item['date_end'] = date_end
        find_item = copy.deepcopy(item)
        item['insert_time'] = datetime.now()
        COLLECTION.update(find_item, {'$set':item}, upsert = True)
        #print item


    

            