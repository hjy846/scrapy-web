from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"^$", views.total_volumn_price, name = 'index'),
    url(r"^total_volumn_price/", views.total_volumn_price, name = 'total_volumn_price'),
]