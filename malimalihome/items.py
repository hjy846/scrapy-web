import scrapy
from scrapy.contrib.pipeline.images import ImagesPipeline

class MalimalihomeItem(scrapy.Item):
    building_name = scrapy.Field()
    price = scrapy.Field()
    bed_room_num = scrapy.Field()
    living_room_num = scrapy.Field()
    size = scrapy.Field()
    link  = scrapy.Field()
    update_time = scrapy.Field()
    remark  = scrapy.Field()
    agent_logo = scrapy.Field()
    photo_num = scrapy.Field()
    _id = scrapy.Field()
    list_insert_time = scrapy.Field()


class ResidenceDetailItem(scrapy.Item):
    _id = scrapy.Field()
    building = scrapy.Field()
    location = scrapy.Field()
    rent = scrapy.Field()
    property_type = scrapy.Field()
    region = scrapy.Field()
    block = scrapy.Field()
    floor = scrapy.Field()
    room = scrapy.Field()
    layout = scrapy.Field()
    size = scrapy.Field()
    net_size = scrapy.Field()
    price = scrapy.Field()
    price_per_ft2 = scrapy.Field()
    rental = scrapy.Field()
    rental_per_ft2 = scrapy.Field()
    age = scrapy.Field()
    lift = scrapy.Field()

    direction = scrapy.Field()
    views = scrapy.Field()
    renovation = scrapy.Field()
    other = scrapy.Field()
    remark = scrapy.Field()
    detail_insert_time = scrapy.Field()
    image_list = scrapy.Field()

#class MaliMaliHomeImagesPipeline(ImagesPipeline):

class ResidenceImageItem(scrapy.Item):
    # ... other item fields ...
    image_urls = scrapy.Field()
    images = scrapy.Field()
    image_paths = scrapy.Field()
