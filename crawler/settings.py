# -*- coding: utf-8 -*-

# Scrapy settings for residence project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'residence'

SPIDER_MODULES = ['crawler.spiders']
NEWSPIDER_MODULE = 'crawler.spiders'

HTTPERROR_ALLOWED_CODES = [100]
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'residence (+http://www.yourdomain.com)'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS=32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY=3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN=16
#CONCURRENT_REQUESTS_PER_IP=16

# Disable cookies (enabled by default)
#COOKIES_ENABLED=False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED=False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'crawler.middlewares.MyCustomSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'crawler.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'crawler.pipelines.ResidencePipeline': 300,
    'crawler.pipelines.ZhongyuanNewPipeline': 400,
    'crawler.pipelines.DsfPipeline': 200,
    'scrapy.pipelines.images.ImagesPipeline': 1
}

IMAGES_STORE = '../web/static/residence_images/'
IMAGES_EXPIRES = 3650

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# NOTE: AutoThrottle will honour the standard settings for concurrency and delay
#AUTOTHROTTLE_ENABLED=True
# The initial download delay
#AUTOTHROTTLE_START_DELAY=5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY=60
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG=False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED=True
#HTTPCACHE_EXPIRATION_SECS=0
#HTTPCACHE_DIR='httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES=[]
#HTTPCACHE_STORAGE='scrapy.extensions.httpcache.FilesystemCacheStorage'

MONGODB_SERVER='127.0.0.1'
MONGODB_PORT=8888

MONGODB_DB_RAW='residence_raw_hour'
MONGODB_COLLECTION_ALL_RESIDENCES='all_residences'
MONGODB_COLLECTION_IMAGE='image_info'

MONGODB_DB='residence_hour'
MONGODB_COLLECTION_NEW_ADD='new_add_residences'
MONGODB_COLLECTION_RESIDENCE_NUM_BY_DAY='residence_num_by_day'
MONGODB_COLLECTION_ZHONGYUAN='zhongyuan'
MONGODB_COLLECTION_ZHONGYUAN_NEW='zhongyuan_new'
MONGODB_COLLECTION_DSF='dsf'
MONGODB_COLLECTION_DSF_RAW='dsf_raw'
MONGODB_COLLECTION_DSF_XIANLOU_RAW='dsf_xianlou_raw'
MONGODB_COLLECTION_DSF_LOUHUA_RAW='dsf_louhua_raw'
MONGODB_COLLECTION_PRICE_TREND='price_trend'
MONGODB_COLLECTION_PRICE_TREND_MONTH='price_trend_by_month'
MONGODB_COLLECTION_PRICE_TREND_BY_RESIDENCE='price_trend_by_residence'

GO_NEXT=True
DOWNLOAD_TIMEOUT=30

INIT_URL="http://www.malimalihome.net/residential?status=1&prepage=10&page=1"
START_URL="http://www.malimalihome.net"

