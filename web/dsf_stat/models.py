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
    insert_date = DateTimeField()
    meta = {'collection':"dsf_raw"}