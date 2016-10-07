from django.shortcuts import render
from django.http import HttpResponse
from models import NewAddResidenceModel
from django.shortcuts import render

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# Create your views here.
def total(request):
    records = NewAddResidenceModel.objects(__raw__ = {'date':{'$gt':'2016-09-25'}}).only('date', 'total').order_by('date')[0:2]
    for r in records:
    	print r.date
    	#print r.total
    return render(request, 'new_residence/total.html', {'username':'hjy846'})
 
def macau(request):

    #records = NewAddResidenceModel.objects

    return render(request, 'new_residence/macau.html', {'username':'hjy846'})

def taipa(request):

    #records = NewAddResidenceModel.objects

    return render(request, 'new_residence/taipa.html', {'username':'hjy846'})

def coloane(request):

    #records = NewAddResidenceModel.objects
    
    return render(request, 'new_residence/coloane.html', {'username':'hjy846'})