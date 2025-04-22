from django.urls import path

from .views import *
from . import views

get_all_transaction_api = TransactionMVS.as_view({
    'get': 'get_all_transaction_api',
})

get_transaction_by_id_api = TransactionMVS.as_view({
    'get': 'get_transaction_by_id_api',
})


urlpatterns = [
    path('', get_all_transaction_api),
    path('<int:id>/', get_transaction_by_id_api),
]