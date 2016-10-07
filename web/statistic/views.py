from django.shortcuts import render
from django.http import HttpResponse
from models import ResidenceNumByDayModel
from django.shortcuts import render

# Create your views here.
def index(request):

    records = ResidenceNumByDayModel.objects

    return render(request, 'stat/index.html', {'username':'hjy846'})
    return HttpResponse("ok")