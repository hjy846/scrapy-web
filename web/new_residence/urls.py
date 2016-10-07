from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"^$", views.total, name = 'index'),
    url(r"^total/", views.total, name = 'total'),
    url(r"^macau/", views.macau, name = 'index'),
    url(r"^taipa/", views.taipa, name = 'index'),
    url(r"^coloane/", views.coloane, name = 'index'),
]