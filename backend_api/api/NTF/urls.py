from django.urls import path

from .views import *
from . import views

get_all_ntfs_api = NTFsMVS.as_view({
    'get': 'get_all_ntfs_api',
})

get_ntfs_by_user_id_api = NTFsMVS.as_view({
    'get': 'get_ntfs_by_user_id_api'
})

get_ntfs_by_id_api = NTFsMVS.as_view({
    'get': 'get_ntfs_by_id_api'
})

add_ntfs_api = NTFsMVS.as_view({
    'post': 'add_ntfs_api'
})

update_staked_api = NTFsMVS.as_view({
    'put': 'update_staked_api'
})

urlpatterns = [
    # path('', get_all_ntfs_api),
    path('get_ntfs_by_user_id_api/', get_ntfs_by_user_id_api),
    path('mint/', add_ntfs_api),
    path('update_staked_api/', update_staked_api),
    path('get_ntfs_by_id_api/<int:id>/', get_ntfs_by_id_api),
]