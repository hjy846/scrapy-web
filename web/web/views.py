# -*- coding:utf-8 -*-  

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.http import HttpResponseRedirect, HttpResponse

# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('passwd', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect("/")
        else:
            #print 'incorrect'
            redirectUrl = '/accounts/login?username=%s&errormsg=%s' % (username, u'错误的账户名或者密码')
            return HttpResponseRedirect(redirectUrl)
    else:
        params = {}
        username = request.GET.get('username', '')
        errormsg = request.GET.get('errormsg', '')
        params['username'] = username
        params['af_name'] = 'autofocus' if username == '' else ''
        params['af_passwd'] = 'autofocus' if username != '' else ''
        params['error'] = True if errormsg else False
        params['errormsg'] = errormsg
        return render(request, 'accounts/login.html', params)

def logout(request):
    username = request.user.username
    auth.logout(request)
    redirectUrl = '/accounts/login?username=%s' % username
    return HttpResponseRedirect(redirectUrl)

def page404(request):
    return render(request, '404.html')
