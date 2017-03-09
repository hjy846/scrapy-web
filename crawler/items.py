#! -*- encoding:utf-8 -*-

import scrapy
from scrapy.contrib.pipeline.images import ImagesPipeline

class ResidenceItem(scrapy.Item):
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

    agent_name = scrapy.Field()
    agent_contact = scrapy.Field()
    agent_company = scrapy.Field()
    agent_address = scrapy.Field()


class ResidenceImageItem(scrapy.Item):
    # ... other item fields ...
    image_urls = scrapy.Field()
    images = scrapy.Field()
    image_paths = scrapy.Field()

class ResidenceRentItem(scrapy.Item):
    building_name = scrapy.Field()
    rent_price = scrapy.Field()
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


class ResidenceRentDetailItem(scrapy.Item):
    _id = scrapy.Field()
    building = scrapy.Field()
    location = scrapy.Field()
    rent_price = scrapy.Field()
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

    agent_name = scrapy.Field()
    agent_contact = scrapy.Field()
    agent_company = scrapy.Field()
    agent_address = scrapy.Field()


class ResidenceRentImageItem(scrapy.Item):
    # ... other item fields ...
    image_urls = scrapy.Field()
    images = scrapy.Field()
    image_paths = scrapy.Field()

class ZhongyuanItem(scrapy.Item):
    # ... other item fields ...
    path = scrapy.Field()
    url = scrapy.Field()

class ZhongyuanNewItem(scrapy.Item):
    # ... other item fields ...
    status = scrapy.Field()
    #BuiltArea
    size = scrapy.Field()
    #Name
    building = scrapy.Field()
    #f_area
    region = scrapy.Field()
    #
    area = scrapy.Field()
    district = scrapy.Field()
    file_type = scrapy.Field()
    prop_type = scrapy.Field()
    #avg_price
    price_per_ft2 = scrapy.Field()
    #prop_name
    block_floor = scrapy.Field()
    #memo
    remark = scrapy.Field()
    #total
    price = scrapy.Field()
    #source_from
    market = scrapy.Field()

    tx_date = scrapy.Field()

    #
    update_time = scrapy.Field()


class DsfItem(scrapy.Item):
    # ... other item fields ...
    remark = scrapy.Field()
    date = scrapy.Field()
    insert_date = scrapy.Field()
    total_stat = scrapy.Field()
    detail_stat = scrapy.Field()
    #0統計全部 1統計現樓 2統計樓花
    stat_type = scrapy.Field()
    
class ParkingItem(scrapy.Item):
    building_name = scrapy.Field()
    price = scrapy.Field()
    link  = scrapy.Field()
    update_time = scrapy.Field()
    remark  = scrapy.Field()
    agent_logo = scrapy.Field()
    photo_num = scrapy.Field()
    _id = scrapy.Field()
    list_insert_time = scrapy.Field()


class ParkingDetailItem(scrapy.Item):
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

    agent_name = scrapy.Field()
    agent_contact = scrapy.Field()
    agent_company = scrapy.Field()
    agent_address = scrapy.Field()

class ParkingImageItem(scrapy.Item):
    # ... other item fields ...
    image_urls = scrapy.Field()
    images = scrapy.Field()
    image_paths = scrapy.Field()

class ParkingRentItem(scrapy.Item):
    building_name = scrapy.Field()
    rent_price = scrapy.Field()
    link  = scrapy.Field()
    update_time = scrapy.Field()
    remark  = scrapy.Field()
    agent_logo = scrapy.Field()
    photo_num = scrapy.Field()
    _id = scrapy.Field()
    list_insert_time = scrapy.Field()


class ParkingRentDetailItem(scrapy.Item):
    _id = scrapy.Field()
    building = scrapy.Field()
    location = scrapy.Field()
    rent_price = scrapy.Field()
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

    agent_name = scrapy.Field()
    agent_contact = scrapy.Field()
    agent_company = scrapy.Field()
    agent_address = scrapy.Field()

class ParkingRentImageItem(scrapy.Item):
    # ... other item fields ...
    image_urls = scrapy.Field()
    images = scrapy.Field()
    image_paths = scrapy.Field()