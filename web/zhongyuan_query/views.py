from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def query(request):
    username = request.user.username
    return render(request, 'zhongyuan_query/query.html', {'username':username})