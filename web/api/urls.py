from django.conf.urls import url
from . import views

urlpatterns = [
	url(r"^$", views.get_residence_num, name = 'get_residence_num'),
	url(r"^get_residence_num/", views.get_residence_num, name = 'get_residence_num'),
	url(r"^get_residence_num_new/", views.get_residence_num_new, name = 'get_residence_num_new'),
    url(r"^get_residence_num_by_month/", views.get_residence_num_by_month, name = 'get_residence_num_by_month'),
    url(r"^get_up_down_num_by_month/", views.get_up_down_num_by_month, name = 'get_up_down_num_by_month'),
    url(r"^get_new_residence_num_by_month/", views.get_new_residence_num_by_month, name = 'get_new_residence_num_by_month'),
	url(r"^get_new_residence_total/", views.get_new_residence_total, name = 'get_new_residence_total'),
	url(r"^get_new_residence_macau/", views.get_new_residence_macau, name = 'get_new_residence_macau'),
	url(r"^get_new_residence_taipa/", views.get_new_residence_taipa, name = 'get_new_residence_taipa'),
	url(r"^get_new_residence_coloane/", views.get_new_residence_coloane, name = 'get_new_residence_coloane'),
	url(r"^all_residence_query/", views.all_residence_query, name = 'all_residence_query'),
    url(r"^zhongyuan_query/", views.zhongyuan_query, name = 'zhongyuan_query'),
    url(r"^dsf_total_volumn_price_query/", views.dsf_total_volumn_price_query, name = 'dsf_total_volumn_price_query'),
    url(r"^dsf_xianlou_volumn_price_query/", views.dsf_xianlou_volumn_price_query, name = 'dsf_xianlou_volumn_price_query'),
    url(r"^dsf_louhua_volumn_price_query/", views.dsf_louhua_volumn_price_query, name = 'dsf_louhua_volumn_price_query'),
    url(r"^get_key_residences_info/", views.get_key_residences_info, name = 'get_key_residences_info'),
    url(r"^get_key_residence/", views.get_key_residence, name = 'get_key_residence'),
    url(r"^get_dsf_detail/", views.get_dsf_detail, name = 'get_dsf_detail')
]