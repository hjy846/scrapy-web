#! -*- encoding:utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from statistic.models import ResidenceNumByDayModel, PriceTrendByMonthModel, KeyResidencesModel
from new_residence.models import NewAddResidenceModel, AllResidenceModel
from zhongyuan_query.models import ZhongyuanModel
from dsf_stat.models import DsfRawModel, DsfXianlouModel, DsfLouhuaModel
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
    date_beg = now - timedelta(days = 60)
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
    date_beg = now - timedelta(days = 60)
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
        if 'image_list_new' in r and len(r['image_list_new']):
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
        #query_params = json.loads(request.GET.get('params'))
        query_params = {}
        building = request.GET.get('building', '')
        if building != '':
            query_params['building'] = building.strip()
        region = request.GET.get('region', 'all')
        if region != 'all':
            query_params['region'] = region
        date_beg = request.GET.get('date_beg', '')
        date_end = request.GET.get('date_end', '')
        if date_beg != '':
            query_params['update_time'] = {'$gte':date_beg}
        if date_end != '':
            if 'update_time' not in query_params:
                query_params['update_time'] = {}
            query_params['update_time']['$lte'] = date_end
        print query_params
        result = ZhongyuanModel.objects(__raw__=query_params).order_by('update_time')
        for res in result:
            ret_dict['data'].append(json.loads(res.to_json()))
        print ret_dict
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
            try:
                item = {'coloane':0}
                #item = {}
                item['date'] = '%s-%s' % (date_beg_format_inner[0:4], date_beg_format_inner[4:6])
                for i in r.total_stat:
                    region = i['region'].split(' ')[0]
                    print region
                    if region == u'澳門半島':
                        item['macau'] = i[target] if i[target] else 0
                    elif region == u'氹仔':
                        item['taipa'] = i[target] if i[target] else 0
                    elif region == u'路環':
                        #pass
                        item['coloane'] = i[target] if i[target] else 0
                    elif region == u'全澳':
                        #pass
                        item['total'] = i[target] if i[target] else 0
                
            except Exception as e:
                print len(r.total_stat)
                print r.total_stat
        else:
            item = {}
            item['date'] = '%s-%s' % (date_beg_format_inner[0:4], date_beg_format_inner[4:6])
            item['total'] = 0
            item['macau'] = 0
            item['taipa'] = 0
            item['coloane'] = 0
        if item['total'] == 0:
            continue
        ret.append(item)
        
    return HttpResponse(json.dumps(ret))

@login_required
def dsf_xianlou_volumn_price_query(request):
    ret_dict = {'errorno':0, 'data':[]}
    target = request.GET.get('query', 'volumn')

    now = datetime.now()
    date_beg = now - timedelta(days = 365 * 6)
    date_beg_str = date_beg.strftime('%Y%m')
    print date_beg_str
    
    records = DsfXianlouModel.objects(__raw__={'date':{"$gte":date_beg_str}}).order_by('-date')
    records_dict = {}
    for r in records:
        records_dict[r['date']] = r

    ret = []
    for date in gen_date(date_beg_str, records[0].date):
        date_beg_format_inner = date
        if date_beg_format_inner in records_dict:
            r = records_dict[date_beg_format_inner]
            try:
                item = {'coloane':0}
                #item = {}
                item['date'] = '%s-%s' % (date_beg_format_inner[0:4], date_beg_format_inner[4:6])
                for i in r.total_stat:
                    region = i['region'].split(' ')[0]
                    print region
                    if region == u'澳門半島':
                        item['macau'] = i[target] if i[target] else 0
                    elif region == u'氹仔':
                        item['taipa'] = i[target] if i[target] else 0
                    elif region == u'路環':
                        #pass
                        item['coloane'] = i[target] if i[target] else 0
                    elif region == u'全澳':
                        #pass
                        item['total'] = i[target] if i[target] else 0
                
            except Exception as e:
                print len(r.total_stat)
                print r.total_stat
        else:
            item = {}
            item['date'] = '%s-%s' % (date_beg_format_inner[0:4], date_beg_format_inner[4:6])
            item['total'] = 0
            item['macau'] = 0
            item['taipa'] = 0
            item['coloane'] = 0
        if item['total'] == 0:
            continue
        ret.append(item)
        
    return HttpResponse(json.dumps(ret))

@login_required
def dsf_louhua_volumn_price_query(request):
    ret_dict = {'errorno':0, 'data':[]}
    target = request.GET.get('query', 'volumn')

    now = datetime.now()
    date_beg = now - timedelta(days = 365 * 6)
    date_beg_str = date_beg.strftime('%Y%m')
    print date_beg_str
    
    records = DsfLouhuaModel.objects(__raw__={'date':{"$gte":date_beg_str}}).order_by('-date')
    records_dict = {}
    for r in records:
        records_dict[r['date']] = r

    ret = []
    for date in gen_date(date_beg_str, records[0].date):
        date_beg_format_inner = date
        if date_beg_format_inner in records_dict:
            r = records_dict[date_beg_format_inner]
            try:
                item = {'coloane':0}
                #item = {}
                item['date'] = '%s-%s' % (date_beg_format_inner[0:4], date_beg_format_inner[4:6])
                for i in r.total_stat:
                    region = i['region'].split(' ')[0]
                    print region
                    if region == u'澳門半島':
                        item['macau'] = i[target] if i[target] else 0
                    elif region == u'氹仔':
                        item['taipa'] = i[target] if i[target] else 0
                    elif region == u'路環':
                        #pass
                        item['coloane'] = i[target] if i[target] else 0
                    elif region == u'全澳':
                        #pass
                        item['total'] = i[target] if i[target] else 0
                
            except Exception as e:
                print len(r.total_stat)
                print r.total_stat
        else:
            item = {}
            item['date'] = '%s-%s' % (date_beg_format_inner[0:4], date_beg_format_inner[4:6])
            item['total'] = 0
            item['macau'] = 0
            item['taipa'] = 0
            item['coloane'] = 0
        if item['total'] == 0:
            continue
        ret.append(item)
        
    return HttpResponse(json.dumps(ret))

@login_required
def get_residence_num_by_month(request):
    records = PriceTrendByMonthModel.objects(__raw__={}).order_by('date')
    ret = []
    for r in records:
        item = {}
        item['date'] = r.date
        item['total'] = r.total if r.total else 0
        item['macau'] = r.total_macau if r.total_macau else 0
        item['taipa'] = r.total_taipa if r.total_taipa else 0
        item['coloane'] = r.total_coloane if r.total_coloane else 0
        item['avg_total'] = r.avg_total if r.avg_total else 0
        item['avg_macau'] = r.avg_macau if r.avg_macau else 0
        item['avg_taipa'] = r.avg_taipa if r.avg_taipa else 0
        item['avg_coloane'] = r.avg_coloane if r.avg_coloane else 0
        ret.append(item)
    
    return HttpResponse(json.dumps(ret))

@login_required
def get_new_residence_num_by_month(request):
    records = PriceTrendByMonthModel.objects(__raw__={}).order_by('date')
    ret = []
    for r in records:
        item = {}
        item['date'] = r.date
        item['new'] = r.new if r.new else 0
        item['new_macau'] = r.new_macau if r.new_macau else 0
        item['new_taipa'] = r.new_taipa if r.new_taipa else 0
        item['new_coloane'] = r.new_coloane if r.new_coloane else 0
        ret.append(item)
    
    return HttpResponse(json.dumps(ret))

@login_required
def get_up_down_num_by_month(request):
    records = PriceTrendByMonthModel.objects(__raw__={}).order_by('date')
    ret = []
    for r in records:
        item = {}
        item['date'] = r.date
        item['up_macau'] = r.up_macau if r.up_macau else 0
        item['up_taipa'] = r.up_taipa if r.up_taipa else 0
        item['up_coloane'] = r.up_coloane if r.up_coloane else 0
        item['down_macau'] = r.down_macau if r.down_macau else 0
        item['down_taipa'] = r.down_taipa if r.down_taipa else 0
        item['down_coloane'] = r.down_coloane if r.down_coloane else 0
        ret.append(item)
    
    return HttpResponse(json.dumps(ret))

@login_required
def get_key_residences_info(request):
    records = KeyResidencesModel.objects.aggregate(*[{"$sort":{"date":1}}, {"$group":{"_id":"$building", "date":{"$push":"$date"}, "total":{"$push":"$total"}, "up":{"$push":"$up"}, "down":{"$push":"$down"}, "avg":{"$push":"$avg"}, "new":{"$push":"$new"}}}])

    ret = []
    for r in records:
        ret.append(r)
    
    return HttpResponse(json.dumps(ret))