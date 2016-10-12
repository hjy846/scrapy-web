from django.shortcuts import render

def query(request):
    return render(request, 'zhongyuan_query/query.html', {'username':'hjy846'})