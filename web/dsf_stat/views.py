from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def total_volumn_price(request):
    return render(request, 'dsf_stat/total_volumn_price.html', {'username':'hjy846'})
