from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def total_volumn_price(request):
    username = request.user.username
    return render(request, 'dsf_stat/total_volumn_price.html', {'username':username})

@login_required
def xianlou_volumn_price(request):
    username = request.user.username
    return render(request, 'dsf_stat/xianlou_volumn_price.html', {'username':username})

@login_required
def louhua_volumn_price(request):
    username = request.user.username
    return render(request, 'dsf_stat/louhua_volumn_price.html', {'username':username})

@login_required
def detail(request):
    username = request.user.username
    return render(request, 'dsf_stat/detail.html', {'username':username})