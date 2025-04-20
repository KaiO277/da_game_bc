from django.urls import path

from .views import *
from . import views

product_get_all_api = ProductMVS.as_view({
    'get': 'product_get_all_api',
})

get_user_detail_user_id_api = UserDetailMVS.as_view({
    'get': 'get_user_detail_user_id_api',
})

update_user_profile_api = UserDetailMVS.as_view({
    'put': 'update_user_profile_api',
})

product_add_api = ProductMVS.as_view({
    'post': 'product_add_api',
})


urlpatterns = [
    path('product_get_all_api/', product_get_all_api, name='product_get_all_api'),
    path('product_add_api/', product_add_api, name='product_add_api'),
    path('users/<int:id>', get_user_detail_user_id_api),
    path('users/update/', update_user_profile_api),
]