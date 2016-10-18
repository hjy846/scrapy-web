# -*- coding: utf-8 -*-
import scrapy
import os
from crawler.items import ZhongyuanItem


class CentalineSpider(scrapy.Spider):
    name = "centaline"
    allowed_domains = ["www.centaline-macau.com"]
    start_urls = (
        'http://www.centaline-macau.com/icms/template.aspx?series=62',
    )

    save_path = './output/zhongyuan'

    def parse(self, response):
        return self.parse_list(response)

    def parse_list(self, response):
        for sel in response.xpath('//form[@name="article"]/select/option/@value')[0:2].extract():
            url = "http://www.centaline-macau.com/icms/template.aspx?series=%s" % sel
            yield scrapy.Request(url, self.get_download_url)

    def get_download_url(self, response):
        for sel in response.xpath('//a/@href').extract():
            if sel.split('.')[-1] == 'pdf':
                download_url = response.urljoin(sel)
                path = '%s/%s/' % (self.save_path, download_url.split('/')[-2:-1][0])
                filename = download_url.split('/')[-1].replace(' ', '_')
                #print path, filename
                if os.path.exists(path + filename):
                    continue
                yield scrapy.Request(download_url, self.parse_save_pdf)

    def parse_save_pdf(self, response):
        #print '*^' * 100
        path = '%s/%s/' % (self.save_path, response.url.split('/')[-2:-1][0])
        if not os.path.exists(path):
            os.makedirs(path)
        file_name = response.url.split('/')[-1].replace('%20', '_')  
        
        with open(path + file_name, 'wb') as fp:
            fp.write(response.body)

        item = ZhongyuanItem()
        item['path'] = path + file_name
        item['url'] = response.url
        yield item
