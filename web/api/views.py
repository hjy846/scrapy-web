#! -*- encoding:utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from statistic.models import ResidenceNumByDayModel
from new_residence.models import NewAddResidenceModel, AllResidenceModel
from zhongyuan_query.models import ZhongyuanModel
from dsf_stat.models import DsfRawModel
from django.shortcuts import render
from bson import json_util

from datetime import datetime, timedelta
import json
import math
import urlparse
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def get_residence_num(request):
    now = datetime.now()
    date_beg = now - timedelta(days = 30)
    date_beg_str = date_beg.strftime('%Y-%m-%d')
    records = ResidenceNumByDayModel.objects(__raw__={'date':{"$gte":date_beg_str}}).order_by('date')

    records_dict = {}
    for r in records:
        records_dict[r['date']] = r
    ret = []
    while date_beg <= now:
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

@login_required
def get_residence_num_new(request):
    now = datetime.now()
    date_beg = now - timedelta(days = 30)
    date_beg_str = date_beg.strftime('%Y-%m-%d')
    records = ResidenceNumByDayModel.objects(__raw__={'date':{"$gte":date_beg_str}}).order_by('date')

    records_dict = {}
    for r in records:
        records_dict[r['date']] = r
    ret = []
    while date_beg <= now:
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

@login_required
def get_new_residence_total(request):
    now = datetime.now()
    yesterday = now - timedelta(days=1)
    region = request.GET.get('region', 'all')
    date_beg = request.GET.get('from', yesterday.strftime('%Y-%m-%d'))
    date_end = request.GET.get('to', now.strftime('%Y-%m-%d'))
    
    result = get_yesterday_new_residence(region, date_beg, date_end)
    #print len(result)
    return HttpResponse(json.dumps(result, default = json_util.default))

@login_required
def get_new_residence_macau(request):
    region = u'澳門'
    
    result = get_yesterday_new_residence(region)
    #print len(result)
    return HttpResponse(json.dumps(result, default = json_util.default))
@login_required
def get_new_residence_taipa(request):
    region = u'氹仔'
    
    result = get_yesterday_new_residence(region)
    #print len(result)
    return HttpResponse(json.dumps(result, default = json_util.default))
@login_required
def get_new_residence_coloane(request):
    region = u'路環'
    
    result = get_yesterday_new_residence(region)
    #print len(result)
    return HttpResponse(json.dumps(result, default = json_util.default))

def get_yesterday_new_residence(region, date_beg, date_end):
    result = get_new_residence(region, date_beg, date_end)
    return result

def get_new_residence(region, date_beg, date_end):
    query_param = {'first_release_time':{'$gte':date_beg, '$lte':date_end}}

    if region == 'macau':
        query_param['info.region'] = u'澳門'
    elif region == 'taipa':
        query_param['info.region'] = u'氹仔'
    elif region == 'coloane':
        query_param['info.region'] = u'路環'

    result = AllResidenceModel.objects(__raw__ = query_param)
    
    ret = []
    for r in result:
        ret_dict = dict(r.info)
        if 'image_list_new' in r:
            ret_dict['image_list'] = r['image_list_new']
            print ret_dict['_id'], ret_dict['building']
            print ret_dict['image_list']
        if len(ret_dict['image_list']):
            ret_dict['building_name'] = u'%s (%s图)' % (ret_dict['building_name'], len(ret_dict['image_list']))
        ret.append(ret_dict)
    return ret

@login_required
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
        print r
        item = r.info
        if 'image_list_new' in r:
            item['image_list'] = r['image_list_new']
        item['price_history'] = r.price_history
        ret_dict['data'].append(item)
    return HttpResponse(json.dumps(ret_dict, default = json_util.default))
    
@login_required
def zhongyuan_query(request):
    ret_dict = {'errorno':0, 'data':[]}
    try:
        query_params = json.loads(request.GET.get('params'))
        print query_params
        result = ZhongyuanModel.objects(__raw__=query_params).order_by('date_beg')
        for res in result:
            ret_dict['data'].append(json.loads(res.to_json()))
    except Exception as e:
        ret_dict['errorno'] = 1
        ret_dict['errormsg'] = repr(e)
        return HttpResponse(json.dumps(ret_dict))

    return HttpResponse(json.dumps(ret_dict, default = json_util.default))

def gen_date(date_beg, date_end):
    year_beg = int(date_beg[0:4])
    month_beg = int(date_beg[4:6]) - 1

    d_beg = date_beg
    d_end = date_end
    while(d_beg <= d_end):
        yield d_beg
        month_beg = (month_beg + 1) % 12
        if month_beg == 0:
            year_beg += 1
        d_beg = '%s%02d' % (year_beg, month_beg + 1)

@login_required
def dsf_total_volumn_price_query(request):
    ret_dict = {'errorno':0, 'data':[]}
    target = request.GET.get('query', 'volumn')

    now = datetime.now()
    date_beg = now - timedelta(days = 365 * 6)
    date_beg_str = date_beg.strftime('%Y%m')
    print date_beg_str
    
    records = DsfRawModel.objects(__raw__={'date':{"$gte":date_beg_str}}).order_by('-date')
    records_dict = {}
    for r in records:
        records_dict[r['date']] = r

    ret = []
    for date in gen_date(date_beg_str, records[0].date):
        date_beg_format_inner = date
        if date_beg_format_inner in records_dict:
            r = records_dict[date_beg_format_inner]
            item = {}
            item['date'] = '%s-%s' % (date_beg_format_inner[0:4], date_beg_format_inner[4:6])
            item['total'] = r.total_stat[3][target] if r.total_stat[3][target] else 0
            item['macau'] = r.total_stat[0][target] if r.total_stat[0][target] else 0
            item['taipa'] = r.total_stat[1][target] if r.total_stat[1][target] else 0
            item['coloane'] = r.total_stat[2][target] if r.total_stat[2][target] else 0
        else:
            item = {}
            item['date'] = '%s-%s' % (date_beg_format_inner[0:4], date_beg_format_inner[4:6])
            item['total'] = 0
            item['macau'] = 0
            item['taipa'] = 0
            item['coloane'] = 0
        
        ret.append(item)
        
    return HttpResponse(json.dumps(ret))