from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def total_volumn_price(request):
    username = request.user.username
    return render(request, 'dsf_stat/total_volumn_price.html', {'username':username})
