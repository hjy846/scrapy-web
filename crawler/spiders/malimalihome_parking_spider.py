# -*- encoding:utf-8 -*-

import scrapy
from crawler.items import ParkingItem, ParkingDetailItem, ParkingImageItem
import sys
import time
import urlparse
import os
from datetime import datetime, timedelta
import json
from scrapy.conf import settings
import logging
import traceback

reload(sys)
sys.setdefaultencoding('utf-8')

class ParkingSpider(scrapy.Spider): 
    name = "parking"
    #allowed_domains = ['xxx.net']
    
    start_urls = []

    def __init__(self, crawl_date = None, region = None, *args, **kwargs):
        super(ParkingSpider, self).__init__(*args, **kwargs)
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

        #处理起始爬取url
        url = settings['INIT_PARKING_URL']
        

        #根据地区爬取
        self.region = region if region != None else 'all'
        self.region_num = self.map_region(self.region)
        if self.region_num != None:
            url += '&region1=%s' % self.region_num

        self.start_urls.append(url)

        #房产列表网页保存路径
        self.list_output_path = './output/list_parking/%s/%s/%s/' % (self.crawl_date, self.region, self.now)
        self.list_output_path = self.list_output_path.strip('\r')
        if not os.path.exists(self.list_output_path):
            os.makedirs(self.list_output_path)

        #房产详情页面保存路径
        self.detail_output_path = './output/detail_parking/%s/%s/%s/' % (self.crawl_date, self.region, self.now)
        self.detail_output_path = self.detail_output_path.strip('\r')
        if not os.path.exists(self.detail_output_path):
            os.makedirs(self.detail_output_path)

        #房产图片保存路径
        self.image_output_path = './output/image_parking/'
        self.image_output_path = self.image_output_path.strip('\r')
        if not os.path.exists(self.image_output_path):
            os.makedirs(self.image_output_path)
        
        self.go_next = settings['GO_NEXT']

    def map_region(self, region):
        if region.lower() == 'macau':
            return 3
        elif region.lower() == 'taipa':
            return 1
        elif region.lower() == 'coloane':
            return 6
        return None
    
    def parse1(self, response):
        print 'parse' * 100
        self.parse_articles_follow_next_page(response)
        self.now = int(time.time())

    #解释房产列表
    def parse_list(self, response):
        result = urlparse.urlparse(response.url)
        params = urlparse.parse_qs(result.query, True)
        filename = 'page_%s' % params['page'][0]
        with open(self.list_output_path + filename, 'wb') as f:
            f.write(response.body)
        for sel in response.xpath('//div[@class="result-list"]'):
            try:
                info_list = sel.xpath('div[@style="float:right"]/div[@class="result-list-c"]/div[@class="result-list-c-type"]/b/text()').extract()
                update_time = info_list[-1].strip()
                #if update_time > self.crawl_date:
                #    pass 
                if update_time < self.crawl_date:
                    self.go_next = False
                    break
                item = ParkingItem()
                item['building_name'] = sel.xpath('div[@style="float:right"]/div[@class="result-list-c"]/div[@class="result-list-c-title"]/a/text()').extract()[0]
                item['link'] = sel.xpath('div[@style="float:right"]/div[@class="result-list-c"]/div[@class="result-list-c-title"]/a/@href').extract()[0]
                item['_id'] = item['link'].split('/')[-1:][0]
                item['price'] = sel.xpath('div[@style="float:right"]/div[@class="result-list-r"]/div[@class="result-list-r-price red"]/text()').re('(\d+)')[0]
                item['price'] = int(item['price'])
                
                item['update_time'] = update_time
                
                item['remark'] = sel.xpath('div[@style="float:right"]/div[@class="result-list-c"]/div[@class="result-list-c-desc"]/text()').extract()
                item['remark'] = item['remark'][0] if len(item['remark']) else ''
                item['agent_logo'] = sel.xpath('div[@style="float:right"]/div[@class="result-list-r"]/div[@class="result-list-r-logo"]/img/@src').extract()[0]
                item['photo_num'] = sel.xpath('div[@class="result-list-l"]/div[@class="list-cover"]/div[@class="total_img"]/text()').extract()
                item['photo_num'] = int(item['photo_num'][0].split()[0]) if len(item['photo_num']) else 0
                #self.fp.write(json.dumps(dict(item), ensure_ascii = False) + '\n')
                #爬取详情页
                item['list_insert_time'] = datetime.now()
                yield scrapy.Request(item['link'], self.parse_detail)
                yield item
            except Exception as e:
                self.logger.error(repr(e))
                print 'error: %s' % repr(e)
                print traceback.format_exc()

        #next_page = response.xpath('//div[@class="result-list"]/div[@style="float:right"]').extract()
        next_page = response.xpath('//div[@class="page result-desc"]/div/div/ul[@class="pagination"]/li/a[@rel="next"]/@href').extract()
        if next_page and self.go_next:
            url = response.urljoin(next_page[0])
            yield scrapy.Request(url, self.parse_list)       


    def parse(self, response):
        #return self.parse_image(response)
        #return self.parse_detail(response)
        return self.parse_list(response)

    def parse_detail(self, response):    
        #保存文件
        filename = '%s.html' % response.url.split('/')[-1:][0]
        with open(self.detail_output_path + filename, 'wb') as f:
            f.write(response.body)

        for sel in response.xpath('//div[@class="module1 left"]'):
            try:
                item = ParkingDetailItem()
                item['building'] = sel.xpath('div[@class="view-title"]/a/text()').extract()
                if len(item['building']):
                    item['building'] = item['building'][0]
                else:
                    item['building'] = sel.xpath('div[@class="view-title"]/text()').extract()[0].strip().split()[0]
                item['location'] = sel.xpath('div[@class="view-address"]/text()').extract()[0]
                item['_id'] = sel.xpath('div[@class="view-no"]/b/text()').extract()[0].split('#')[-1:][0]
                item['rent'] = sel.xpath('div[@class="view-price"]/div[@class="view-price-div view-price-yellow"]/div/text()').extract()[0].strip('$').strip('-')
                #item['property_type'] = sel.xpath('div[@class="view-photo"]/div[@class="photo-small slick-initialized slick-slider"]/div[@class="slick-list draggable"]/div[@class="slick-track"]/div[@class="slick-slide slick-current slick-active"]/div[@class="image-border"]/div/center/img/@src').extract()
                info_list_nodes = sel.xpath('div[@class="view-desc"]/div/table/tr')
                info_list = []
                for x in info_list_nodes:
                    for y in x.xpath('td'):
                        info = y.xpath('text()').extract()
                        if len(info):
                            info_list.append(info[0])
                        else:
                            info_list.append("")

                item['property_type'] = info_list[0].strip().strip('-')
                item['region'] = info_list[1].strip().strip('-')
                item['block'] = info_list[2].strip().strip('-')
                item['floor'] = info_list[3].strip().strip('-')
                item['room'] = info_list[4].strip().strip('-')
                item['layout'] = info_list[5].strip().strip('-')
                item['size'] = info_list[6].strip().strip('-').split()
                if len(item['size']):
                    item['size'] = float(item['size'][0])
                else: item['size'] = 0
                item['net_size'] = info_list[7].strip().strip('-').split()
                if len(item['net_size']):
                    item['net_size'] = float(item['net_size'][0])
                else: item['net_size'] = 0
                item['price'] = info_list[8].strip().strip('-').strip('$').split('\r\n')[0]
                if item['price'] != "":
                    item['price'] = float(item['price'])
                item['price_per_ft2'] = info_list[9].strip().strip('-').strip('$').split(u'\u5143')[0]
                if item['price_per_ft2'] != "":
                    item['price_per_ft2'] = float(item['price_per_ft2'])
                item['rental'] = info_list[10].strip().strip('-')
                item['rental_per_ft2'] = info_list[11].strip().strip('-')
                item['age'] = info_list[12].strip().strip('-').split()
                if len(item['age']):
                    item['age'] = int(item['age'][0])
                else:item['age'] = 0
                item['lift'] = info_list[13].strip().strip('-')
                item['direction'] = info_list[14].strip().strip('-')
                item['views'] = info_list[15].strip().strip('-')
                item['renovation'] = info_list[16].strip().strip('-')
                item['other'] = info_list[17].strip().strip('-')
                item['remark'] = info_list[18].strip().strip('-')
                item['detail_insert_time'] = datetime.now()
                item['image_list'] = sel.xpath('div[@class="view-photo"]/div[@class="photo-big"]/a/@href').extract()
                item['agent_name'] = response.xpath('//div[@class="view-agent-desc-contact"]/text()').extract()
                if len(item['agent_name']):
                    item['agent_name'] = item['agent_name'][0].strip()
                else:  item['agent_name'] = ""
                
                item['agent_contact'] = response.xpath('//span[@class="view-agent-desc-phone result-list-b-phone-shown"]/text()').extract()
                if len(item['agent_contact']):
                    item['agent_contact'] = item['agent_contact'][0].strip()
                else:  item['agent_contact'] = ""

                item['agent_company'] = response.xpath('//div[@class="view-agent-name"]/b/text()').extract()
                if len(item['agent_company']):
                    item['agent_company'] = item['agent_company'][0].strip()
                else:  item['agent_company'] = ""

                item['agent_address'] = response.xpath('//div[@class="view-agent-desc-adr"]/text()').extract()
                if len(item['agent_address']):
                    item['agent_address'] = item['agent_address'][0].strip()
                else:  item['agent_address'] = ""

                yield item

                image_item = ParkingImageItem()
                image_item['image_urls'] = item['image_list']
                #yield image_item
            except Exception as e:
                self.logger.error(response.url)
                self.logger.error(repr(e))
                print response.url
                print 'error: %s' % repr(e)
                print traceback.format_exc()

    def parse_image(self, response):
        item = ParkingImageItem()
        item['image_urls'] = ["http://media.xxx.net/images/props/001/216/082/2/570431.jpeg", 
        "http://media.xxx.net/images/props/001/216/082/1/570432.jpeg"]
        yield item
        
