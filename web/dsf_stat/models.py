from __future__ import unicode_literals

from django.db import models

from mongoengine import *
from django.conf import settings

connect(settings.MONGO_DB, port = 8888)

# Create your models here.
class DsfRawModel(Document):
    date = StringField(required = True)
    detail_stat = ListField()
    total_stat = ListField()
    remark = StringField()
    stat_type = StringField()
    insert_date = DateTimeField()
    meta = {'collection':"dsf_raw"}

class DsfXianlouModel(Document):
    date = StringField(required = True)
    detail_stat = ListField()
    total_stat = ListField()
    remark = StringField()
    stat_type = StringField()
    insert_date = DateTimeField()
    meta = {'collection':"dsf_xianlou_raw"}

class DsfLouhuaModel(Document):
    date = StringField(required = True)
    detail_stat = ListField()
    total_stat = ListField()
    remark = StringField()
    stat_type = StringField()
    insert_date = DateTimeField()
    meta = {'collection':"dsf_louhua_raw"}

class DsfStatModel(Document):
    date = StringField(required = True)
    dsf_type = StringField()
    age = DictField()
    price = DictField()
    region = DictField()
    region_price = DictField()
    region_size = DictField()
    meta = {'collection':"dsf_stat"}
