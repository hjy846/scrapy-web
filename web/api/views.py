#! -*- encoding:utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from statistic.models import ResidenceNumByDayModel
from new_residence.models import NewAddResidenceModel, AllResidenceModel
from django.shortcuts import render
from bson import json_util

from datetime import datetime, timedelta
import json
import math

# Create your views here.
def get_residence_num(request):
    now = datetime.now()
    date_beg = now - timedelta(days = 30)
    date_beg_str = date_beg.strftime('%Y-%m-%d')
    records = ResidenceNumByDayModel.objects(__raw__={'date':{"$gte":date_beg_str}}).order_by('date')

    records_dict = {}
    for r in records:
        records_dict[r['date']] = r
    ret = []
    while date_beg < now:
        date_beg_format_inner = date_beg.strftime("%Y-%m-%d")
        if date_beg_format_inner in records_dict:
            r = records_dict[date_beg_format_inner]
        else:
            r = ResidenceNumByDayModel()
            r.date = date_beg_format_inner
        item = {}
        item['date'] = r.date
        item['total'] = r.total if r.total else 0
        item['macau'] = r.macau if r.macau else 0
        item['taipa'] = r.taipa if r.taipa else 0
        item['coloane'] = r.coloane if r.coloane else 0
        ret.append(item)
        date_beg += timedelta(days = 1)
    return HttpResponse(json.dumps(ret))


def get_residence_num_new(request):
    now = datetime.now()
    date_beg = now - timedelta(days = 30)
    date_beg_str = date_beg.strftime('%Y-%m-%d')
    records = ResidenceNumByDayModel.objects(__raw__={'date':{"$gte":date_beg_str}}).order_by('date')

    records_dict = {}
    for r in records:
        records_dict[r['date']] = r
    ret = []
    while date_beg < now:
        date_beg_format_inner = date_beg.strftime("%Y-%m-%d")
        if date_beg_format_inner in records_dict:
            r = records_dict[date_beg_format_inner]
        else:
            r = ResidenceNumByDayModel()
            r.date = date_beg_format_inner
        item = {}
        item['date'] = r.date
        item['total_new'] = r.total_new if r.total_new else 0
        item['macau_new'] = r.macau_new if r.macau_new else 0
        item['taipa_new'] = r.taipa_new if r.taipa_new else 0
        item['coloane_new'] = r.coloane_new if r.coloane_new else 0
        ret.append(item)

        date_beg += timedelta(days = 1)
    return HttpResponse(json.dumps(ret))

def get_new_residence_total(request):
    region = 'total'
    
    result = get_yesterday_new_residence(region)
    #print len(result)
    return HttpResponse(json.dumps(result, default = json_util.default))

def get_new_residence_macau(request):
    region = u'澳門'
    
    result = get_yesterday_new_residence(region)
    #print len(result)
    return HttpResponse(json.dumps(result, default = json_util.default))

def get_new_residence_taipa(request):
    region = u'氹仔'
    
    result = get_yesterday_new_residence(region)
    #print len(result)
    return HttpResponse(json.dumps(result, default = json_util.default))

def get_new_residence_coloane(request):
    region = u'路環'
    
    result = get_yesterday_new_residence(region)
    #print len(result)
    return HttpResponse(json.dumps(result, default = json_util.default))

def get_yesterday_new_residence(region):
    now = datetime.now()
    date_beg = now - timedelta(days = 1)
    date_beg_str = date_beg.strftime('%Y-%m-%d')
    result = get_new_residence(region, date_beg_str)
    return result

def get_new_residence(region, date_beg):
    query_param = {'first_release_time':{'$gte':date_beg}}

    if region != 'total':
        query_param['info.region'] = region

    result = AllResidenceModel.objects(__raw__ = query_param)
    ret = []
    for r in result:
        ret.append(dict(r.info))
    return ret

def all_residence_query(request):
    ret_dict = {'errorno':0, 'data':[], 'total':0}
    try:
        query_params = json.loads(request.GET.get('params'))
        page = int(request.GET.get('page', 1))
        count = int(request.GET.get('count', 10))
        beg = (page - 1) * count
        end = page * count
    
        ret_dict['total'] = AllResidenceModel.objects(__raw__=query_params).count()
        ret_dict['total_page'] = math.ceil(ret_dict['total'] * 1.0 / count)
        ret_dict['page'] = page
        result = AllResidenceModel.objects(__raw__=query_params).order_by('info.price_per_ft2')[beg:end]
    except Exception as e:
        ret_dict['errorno'] = 1
        ret_dict['errormsg'] = repr(e)
        return HttpResponse(json.dumps(ret_dict))

    for r in result:
        item = r.info
        item['price_history'] = r.price_history
        ret_dict['data'].append(item)
    return HttpResponse(json.dumps(ret_dict, default = json_util.default))