from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"^$", views.total_volumn_price, name = 'index'),
    url(r"^total_volumn_price/", views.total_volumn_price, name = 'total_volumn_price'),
    url(r"^xianlou_volumn_price/", views.xianlou_volumn_price, name = 'xianlou_volumn_price'),
    url(r"^louhua_volumn_price/", views.louhua_volumn_price, name = 'louhua_volumn_price'),
    url(r"^detail/", views.detail, name = 'detail'),
]