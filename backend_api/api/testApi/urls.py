from django.urls import path

from .views import *
from . import views



get_user_detail_user_id_api = UserDetailMVS.as_view({
    'get': 'get_user_detail_user_id_api',
})

update_user_profile_api = UserDetailMVS.as_view({
    'put': 'update_user_profile_api',
})

get_user_detail_api = UserDetailMVS.as_view({
    'get': 'get_user_detail_api',
})

delete_user_profile_api = UserDetailMVS.as_view({
    'delete': 'delete_user_profile_api',
})

urlpatterns = [
    path('users/<int:id>/', get_user_detail_user_id_api),
    path('users/update/', update_user_profile_api),
    path('users/', get_user_detail_api),
    path('users/delete/<int:id>/', delete_user_profile_api),
]