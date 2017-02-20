# encoding:utf-8

from django.shortcuts import render
from django.http import HttpResponse
from models import ResidenceNumByDayModel
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def index(request):
    #records = ResidenceNumByDayModel.objects
    username = request.user.username
    return render(request, 'stat/index.html', {'username':username})

#按月统计放盘数
@login_required
def total_release_by_month(request):
    #records = ResidenceNumByDayModel.objects
    username = request.user.username
    return render(request, 'stat/total_release_by_month.html', {'username':username})

#涨跌盘数量
@login_required
def up_down(request):
    #records = ResidenceNumByDayModel.objects
    username = request.user.username
    return render(request, 'stat/up_down.html', {'username':username})