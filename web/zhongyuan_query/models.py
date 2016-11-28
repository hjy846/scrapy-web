from __future__ import unicode_literals

from django.db import models

from mongoengine import *
from django.conf import settings

connect(settings.MONGO_DB, port = settings.MONGO_PORT)

# Create your models here.
class ZhongyuanModel(Document):
    block_floor = StringField()
    building = StringField()
    update_time = StringField()
    market = StringField()
    price = IntField()
    price_per_ft2 = IntField()
    region = StringField()
    remark = StringField()
    size = IntField()
    insert_time = DateTimeField()

    status = StringField()
    district = StringField()
    area = StringField()
    file_type = StringField()
    prop_type = StringField()
    tx_date  = StringField()

    meta = {'collection':"zhongyuan_new"}