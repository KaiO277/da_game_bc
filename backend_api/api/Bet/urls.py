from django.urls import path

from .views import *
from . import views

get_all_bet_api = BetMVS.as_view({
    'get': 'get_all_bet_api',
})
get_bet_by_id_api = BetMVS.as_view({
    'get': 'get_bet_by_id_api',
})

add_bet_api = BetMVS.as_view({
    'post': 'add_bet_api',
})

urlpatterns = [
    path('', get_all_bet_api),
    path('<int:id>/', get_bet_by_id_api),
    path('add/', add_bet_api),
]