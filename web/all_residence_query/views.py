#! -*- encoding:utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from new_residence.models import AllResidenceModel
from django.shortcuts import render
from bson import json_util

from datetime import datetime, timedelta
import json

# Create your views here.
def query(request):
    return render(request, 'all_residence_query/query.html', {'username':'hjy846'})