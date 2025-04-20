from django.conf.urls import include
from django.urls import path

from rest_framework import permissions

from .serializers import MyTokenObtainPairView
from .views import UserMeAPIView
from .views import *


urlpatterns = [
    #
    path('', include('api.testApi.urls')),
    # path('try/', include('api.try.urls')),

    #
    path('auth/google/', GoogleView.as_view(), name='google'),
    path('login/', LoginAPIView.as_view(), name='api-login'),
    path('auth/login_admin/', LoginAdminAPIView.as_view(), name='api-login-admin'),
    path('register/', RegisterAPIView.as_view(), name='api-register'),
    path('user/delete_user_api/', UserDeleteAPIView.as_view(), name='delete_user_api'),
]
