from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta

# Create your views here.
@login_required
def query(request):
    username = request.user.username
    now = datetime.now()
    yesterday = now - timedelta(days=1)
    return render(request, 'zhongyuan_query/query.html', {'username':username, 'date_beg':'2016-01-01', 'date_end':now.strftime('%Y-%m-%d')})