from django.conf.urls import url
from . import views

urlpatterns = [
	url(r"^$", views.get_residence_num, name = 'get_residence_num'),
	url(r"^get_residence_num/", views.get_residence_num, name = 'get_residence_num'),
	url(r"^get_residence_num_new/", views.get_residence_num_new, name = 'get_residence_num_new'),
	url(r"^get_new_residence_total/", views.get_new_residence_total, name = 'get_new_residence_total'),
	url(r"^get_new_residence_macau/", views.get_new_residence_macau, name = 'get_new_residence_macau'),
	url(r"^get_new_residence_taipa/", views.get_new_residence_taipa, name = 'get_new_residence_taipa'),
	url(r"^get_new_residence_coloane/", views.get_new_residence_coloane, name = 'get_new_residence_coloane'),
	url(r"^all_residence_query/", views.all_residence_query, name = 'all_residence_query'),
    url(r"^zhongyuan_query/", views.zhongyuan_query, name = 'zhongyuan_query'),
    url(r"^dsf_total_volumn_price_query/", views.dsf_total_volumn_price_query, name = 'dsf_total_volumn_price_query')
]