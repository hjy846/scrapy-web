from django.shortcuts import render
from django.http import HttpResponse
from models import NewAddResidenceModel
from django.shortcuts import render
from datetime import datetime, timedelta

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def total(request):
    #records = NewAddResidenceModel.objects(__raw__ = {'date':{'$gt':'2016-09-25'}}).only('date', 'total').order_by('date')[0:2]
    #for r in records:
    #	print r.date
    	#print r.total
    username = request.user.username
    now = datetime.now()
    yesterday = now - timedelta(days=1)
    return render(request, 'new_residence/total.html', {'username':username, 'date_beg':yesterday.strftime('%Y-%m-%d'), 'date_end':now.strftime('%Y-%m-%d')})
 
@login_required
def macau(request):

    #records = NewAddResidenceModel.objects
    username = request.user.username
    return render(request, 'new_residence/macau.html', {'username':username})

@login_required
def taipa(request):

    #records = NewAddResidenceModel.objects
    username = request.user.username
    return render(request, 'new_residence/taipa.html', {'username':username})

@login_required
def coloane(request):

    #records = NewAddResidenceModel.objects
    username = request.user.username
    return render(request, 'new_residence/coloane.html', {'username':username})