from django.urls import path

from .views import *
from . import views

get_all_race_api = RaceMVS.as_view({
    'get': 'get_all_race_api',
})

get_race_by_id_api = RaceMVS.as_view({
    'get': 'get_race_by_id_api',
})

urlpatterns = [
    path('', get_all_race_api),
    path('<int:id>/', get_race_by_id_api),
]