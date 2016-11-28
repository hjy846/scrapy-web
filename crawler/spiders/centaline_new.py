# -*- coding: utf-8 -*-
import scrapy
import json
from datetime import datetime, timedelta
from crawler.items import ZhongyuanNewItem
import os


class CentalineNewSpider(scrapy.Spider):
    name = "centaline_new"
    allowed_domains = ["mo.centanet.com"]
    start_urls = ()

    def __init__(self):
        now = datetime.now()
        self.save_path = './output/zhongyuan_new'
        self.now = now.strftime('%Y%m%d')
        self.now_minite = now.strftime('%Y%m%d_%H%M')
        self.output_path = '%s/%s/%s/' % (self.save_path, self.now, self.now_minite)
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)


    def start_requests(self):
        #beg_date = datetime.strptime('2001-03-31', '%Y-%m-%d')
        beg_date = datetime.now()
        #print '*' * 100
        month = beg_date.month + 12
        month -= 2
        year = beg_date.year
        if month <= 12:
            year -= 1
        else:
            month %= 12
        
        beg_date = beg_date.replace(year = year)
        beg_date = beg_date.replace(month = month)
        beg_date = beg_date.replace(day = 1)
        print beg_date.strftime('%Y-%m-%d')

        end_date = datetime.now()
        print end_date.strftime('%Y-%m-%d')
        url = 'http://mo.centanet.com/MODataCharts/Api/TransactionData/GetList?BeginDate=' + beg_date.strftime('%Y-%m-%d') + \
            '&District=&EndDate=' + end_date.strftime('%Y-%m-%d') + \
            '&FileType=%E4%BD%8F%E5%AE%85&Name=&OrderBy=+ID+desc&PageIndex=1&PageSize=100&PropType=S'
    
        yield scrapy.Request(url, self.parse_list, headers = {'Accept':'Application/json,text/plain,*/*'})
        

    def parse(self, response):
        for url in self.start_urls:
            yield scrapy.Request(url, self.parse_list, headers = {'Accept':'Application/json,text/plain,*/*'})

    def parse_list(self, response):
        data = json.loads(response.body)

        with open(self.output_path + str(data['PageIndex']) + '.json', 'wb') as f:
            f.write(response.body)

        for list_data in data['InnerList']:
            item = ZhongyuanNewItem()
            item['status'] = list_data['Status']
            item['size'] = list_data['BuiltArea']
            item['building'] = list_data['Name']
            item['district'] = list_data['District']
            item['area'] = list_data['Area']
            item['region'] = list_data['FArea']
            item['file_type'] = list_data['FileType']
            item['prop_type'] = list_data['PropType']
            item['price_per_ft2'] = list_data['AvgPrice']
            item['block_floor'] = list_data['PropName']
            item['remark'] = list_data['Memo']
            item['price'] = list_data['Total']
            item['market'] = list_data['SourceFrom']
            item['tx_date'] = list_data['TxDate']
            item['update_time'] = item['tx_date'].strip()[0:10]
            yield item
        if data['HasNextPage']:
            new_url = []
            for part in response.url.split('&'):
                if part.find('PageIndex=') != -1:
                    num = data['PageIndex'] + 1
                    new_url.append('PageIndex=%d' % num)
                else:
                    new_url.append(part)
            new_url = '&'.join(new_url)
            yield scrapy.Request(new_url, self.parse_list, headers = {'Accept':'Application/json,text/plain,*/*'})
        
