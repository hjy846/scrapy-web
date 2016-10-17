from django.shortcuts import render
from django.http import HttpResponse
from models import ResidenceNumByDayModel
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def index(request):

    records = ResidenceNumByDayModel.objects
    username = request.user.username
    return render(request, 'stat/index.html', {'username':username})