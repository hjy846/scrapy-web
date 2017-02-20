from django.conf.urls import url
from . import views

urlpatterns = [
	url(r"^$", views.index, name = 'index'),
	url(r"^index/", views.index, name = 'index'),
    url(r"^total_release_by_month/", views.total_release_by_month, name = 'total_release_by_month'),
    url(r"^up_down/", views.up_down, name = 'up_down'),
]