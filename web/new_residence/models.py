#! -*- encoding:utf-8 -*-

from django.db import models

from mongoengine import *
from django.conf import settings

connect(settings.MONGO_DB, port = settings.MONGO_PORT)

# Create your models here.
class NewAddResidenceModel(Document):
    date = StringField(required = True)
    total = ListField()
    macau = ListField()
    taipa = ListField()
    coloane = ListField()
    
    meta = {'collection':"new_add_residences"}

class AllResidenceModel(Document):
    create_time = DateTimeField()
    update_time = DateTimeField()
    first_release_time = StringField()
    price_history = ListField()
    info = DictField()
    meta = {'collection':"all_residences"}
