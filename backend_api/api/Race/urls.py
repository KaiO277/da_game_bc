from django.urls import path

from .views import *
from . import views

get_all_race_api = RaceMVS.as_view({
    'get': 'get_all_race_api',
})

get_race_by_id_api = RaceMVS.as_view({
    'get': 'get_race_by_id_api',
})

add_race_api = RaceMVS.as_view({
    'post': 'add_race_api'
})

update_race_status_api = RaceMVS.as_view({
    'put': 'update_race_status_api'
})

delete_race_api = RaceMVS.as_view({
    'delete': 'delete_race_api'
})

urlpatterns = [
    path('', get_all_race_api),
    path('<int:id>/', get_race_by_id_api),
    path('add/', add_race_api),
    path('update/<int:id>/', update_race_status_api),
    path('delete/<int:id>/', delete_race_api),
]