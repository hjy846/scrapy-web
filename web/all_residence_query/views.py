#! -*- encoding:utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from new_residence.models import AllResidenceModel
from django.shortcuts import render
from bson import json_util

from datetime import datetime, timedelta
import json
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def query(request):
    username = request.user.username
    now = datetime.now()
    beg = now - timedelta(days = 30)
    return render(request, 'all_residence_query/query.html', {'username':username, 'date_beg':beg.strftime('%Y-%m-%d'), 'date_end':now.strftime('%Y-%m-%d')})
