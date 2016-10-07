from __future__ import unicode_literals

from django.db import models

from mongoengine import *


connect('malimalihome', port = 8888)

# Create your models here.
class ResidenceNumByDayModel(Document):
    date = StringField(required = True)
    total = IntField()
    total_new = IntField()
    macau = IntField()
    macau_new = IntField()
    taipa = IntField()
    taipa_new = IntField()
    coloane = IntField()
    coloane_new = IntField()
    insert_time = DateTimeField()
    meta = {'collection':"residence_num_by_day"}

    