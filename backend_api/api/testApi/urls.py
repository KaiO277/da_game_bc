from django.urls import path

from .views import *
from . import views

product_get_all_api = ProductMVS.as_view({
    'get': 'product_get_all_api',
})

urlpatterns = [
    path('product_get_all_api/', product_get_all_api, name='product_get_all_api'),
]