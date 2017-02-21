from __future__ import unicode_literals

from django.db import models

from mongoengine import *
from django.conf import settings

connect(settings.MONGO_DB, port = 8888)

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

class PriceTrendByMonthModel(Document):
    update_time = DateTimeField()
    date = StringField()
    unchange = IntField()
    up = IntField()
    down = IntField()
    new = IntField()
    total = IntField()
    data = ListField()

    unchange_macau = IntField()
    up_macau = IntField()
    down_macau = IntField()
    new_macau = IntField()
    total_macau = IntField()
    data_macau = ListField()

    unchange_taipa = IntField()
    up_taipa = IntField()
    down_taipa = IntField()
    new_taipa = IntField()
    total_taipa = IntField()
    data_taipa = ListField()

    unchange_coloane = IntField()
    up_coloane = IntField()
    down_coloane = IntField()
    new_coloane = IntField()
    total_coloane = IntField()
    data_coloane = ListField()

    avg_total = IntField()
    avg_macau = IntField()
    avg_taipa = IntField()
    avg_coloane = IntField()
    
    meta = {'collection':"price_trend_by_month"}
