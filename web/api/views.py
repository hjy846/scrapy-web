#! -*- encoding:utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from statistic.models import ResidenceNumByDayModel, PriceTrendByMonthModel, KeyResidencesModel
from new_residence.models import NewAddResidenceModel, AllResidenceModel
from zhongyuan_query.models import ZhongyuanModel
from dsf_stat.models import DsfRawModel, DsfXianlouModel, DsfLouhuaModel, DsfStatModel
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
        query_type = request.GET.get('query_type', 'query_by_sql')
        if query_type == 'query_by_sql':
            query_params = json.loads(request.GET.get('sql'))
            page = int(request.GET.get('page', 1))
            count = int(request.GET.get('count', 10))
            beg = (page - 1) * count
            end = page * count
        
            ret_dict['total'] = AllResidenceModel.objects(__raw__=query_params).count()
            ret_dict['total_page'] = math.ceil(ret_dict['total'] * 1.0 / count)
            ret_dict['page'] = page
            result = AllResidenceModel.objects(__raw__=query_params).order_by('info.price_per_ft2')[beg:end]
        elif query_type == 'query':
            query_params = {}
            page = int(request.GET.get('page', 1))
            count = int(request.GET.get('count', 10))
            beg = (page - 1) * count
            end = page * count

            building = request.GET.get('building', '')
            if building:
                query_params['info.building'] = {'$regex':building}

            region = request.GET.get('region', '')
            if region:
                query_params['info.region'] = region

            date_beg = request.GET.get('date_beg', '')
            date_end = request.GET.get('date_end', '')

            if date_beg or date_end:
                query_params['info.update_time'] = {}
                if date_beg:
                    query_params['info.update_time']['$gte'] = date_beg
                if date_end:
                    query_params['info.update_time']['$lte'] = date_end
            
            price_low = request.GET.get('price_low', 0)
            price_high = request.GET.get('price_high', 0)
            if price_low or price_high:
                query_params['info.price'] = {}
                if price_low:
                    query_params['info.price']['$gte'] = int(price_low)
                if price_high:
                    query_params['info.price']['$lte'] = int(price_high)

            price_per_ft2_low = request.GET.get('price_per_ft2_low', 0)
            price_per_ft2_high = request.GET.get('price_per_ft2_high', 0)
            if price_per_ft2_low or price_per_ft2_high :
                query_params['info.price_per_ft2'] = {}
                if price_per_ft2_low:
                    query_params['info.price_per_ft2']['$gte'] = int(price_per_ft2_low)
                if price_per_ft2_high:
                    query_params['info.price_per_ft2']['$lte'] = int(price_per_ft2_high)

            size_low = request.GET.get('size_low', 0)
            size_high = request.GET.get('size_high', 0)
            if size_low or size_high:
                query_params['info.size'] = {}
                if size_low:
                    query_params['info.size']['$gte'] = int(size_low)
                if size_high:
                    query_params['info.size']['$lte'] = int(size_high)
            
            order_by = 'info.price_per_ft2'
            order = request.GET.get('sort', 'price-per-ft2-low-high')
            if order == 'price-per-ft2-high-low':
                order_by = '-info.price_per_ft2'
            elif order == 'price-low-high':
                order_by = 'info.price'
            elif order == 'price-high-low':
                order_by = '-info.price'
            elif order == 'update-time':
                order_by = '-info.update_time'
            
            print query_params
            ret_dict['total'] = AllResidenceModel.objects(__raw__=query_params).count()
            ret_dict['total_page'] = math.ceil(ret_dict['total'] * 1.0 / count)
            ret_dict['page'] = page
            result = AllResidenceModel.objects(__raw__=query_params).order_by(order_by)[beg:end]
        else:
            ret_dict['errorno'] = 1
            ret_dict['errormsg'] = repr(e)
            return HttpResponse(json.dumps(ret_dict))
    except Exception as e:
        print e
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
                    #print region
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
                    #print region
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
                    #print region
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
    
    query_buildings = [u'裕華大廈', u'保利達花園', u'亨達大廈', u'鴻發花園', u'綠楊花園', u'金海山花園', u'海名居', u'海天居', u'寰宇天下', u'君悅灣', u'太子花城', u'濠庭都會', u'鴻業大廈', u'廣福安花園', u'金利達花園']

    ret = query_key_residences(query_buildings)
    
    return HttpResponse(json.dumps(ret))

@login_required
def get_key_residence(request):
    query_building = request.GET.get('query_building', '')
    if not query_building:
        ret = {}
    else:
        try:
            ret = query_key_residences([query_building])[0]
        except Exception as e:
            ret = {}
    
    return HttpResponse(json.dumps(ret))

def query_key_residences(query_buildings):
    records = KeyResidencesModel.objects(__raw__={'building':{"$in":query_buildings}}).aggregate(*[{"$sort":{"date":1}}, {"$group":{"_id":"$building", "date":{"$push":"$date"}, "total":{"$push":"$total"}, "up":{"$push":"$up"}, "down":{"$push":"$down"}, "avg":{"$push":"$avg"}, "new":{"$push":"$new"}}}])

    ret = []
    for r in records:
        ret.append(r)
    return ret

@login_required
def get_dsf_detail(request):
    ret = {}
    dsf_type = request.GET.get('dsf_type', 'total')
    date = request.GET.get('date', '201701')
    
    records = DsfStatModel.objects(__raw__={'date':date, 'dsf_type':dsf_type})
    if len(records) == 0:
        HttpResponse(json.dumps(ret)) 

    age_categories = ['<=5', '06-10', '11-20', '21-30', '> 30']
    region_categories = []
    price_categories = []

    age = []
    region = []
    region_size = []
    region_price = []
    price = []

    for i in age_categories:
        if i in records[0]['age']:
            age.append(records[0]['age'][i])
        else: age.append(0)

    age_categories_desc = ['5年或以下', '6-10年', '11-20年', '21-30年', '大於30年']

    price_list = [(int(i[0]), i[1]) for i in records[0]['price'].items()]
    price_list_sort_by_price = sorted(price_list, key = lambda x:x[0])
    #print price_list_sort_by_price
    for i in price_list_sort_by_price:
        price_categories.append(str(i[0]) + '萬/平米')
        price.append(i[1])


    for i in records[0]['region']:
        region_categories.append(i)
        region.append(records[0]['region'][i])
        region_price.append(records[0]['region_price'][i])
        region_size.append(records[0]['region_size'][i])
        #print

    total_price_list = [(int(i[0]), i[1]) for i in records[0]['total_price'].items()]
    total_price_list_sort_by_price = sorted(total_price_list, key = lambda x:x[0])
    total_price = []
    total_price_categories = []

    for i in total_price_list_sort_by_price:
        total_price_categories.append(str(i[0]) + '萬+')
        total_price.append(i[1])

    ret['age_categories'] = age_categories_desc
    ret['age'] = age
    ret['price_categories'] = price_categories
    ret['price'] = price
    ret['region_categories'] = region_categories
    ret['region'] = region
    ret['region_price'] = region_price
    ret['region_size'] = region_size
    ret['date'] = date
    ret['total_price_categories'] = total_price_categories
    ret['total_price'] = total_price
         
    return HttpResponse(json.dumps(ret))
