from django.conf.urls import include
from django.urls import path

from rest_framework import permissions

from .serializers import MyTokenObtainPairView
from .views import UserMeAPIView
from .views import *
from .views import register_or_login_wallet 
from .views import login, check_username_exists

urlpatterns = [
    #
    path('', include('api.testApi.urls')),
    path('nfts/', include('api.NTF.urls')),
    path('race/', include('api.Race.urls')),
    path('bets/', include('api.Bet.urls')),
    path('transactions/', include('api.Transaction.urls')),

    #
    path('auth/google/', GoogleView.as_view(), name='google'),
    path('login/', login),
    path('register/', register_or_login_wallet),
    path('auth/login_admin/', LoginAdminAPIView.as_view(), name='api-login-admin'),
    path('register/', RegisterAPIView.as_view(), name='api-register'),
    path('check-username/', check_username_exists, name='check-username'),
    path('user/delete_user_api/', UserDeleteAPIView.as_view(), name='delete_user_api'),
]
