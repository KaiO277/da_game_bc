from django.conf.urls import include
from django.urls import path

from rest_framework import permissions

from .serializers import MyTokenObtainPairView
from .views import *

# user_get_list_all_api = UserMVS.as_view({
#     'get': 'user_get_list_all_api',
# })

# user_get_count_api = UserMVS.as_view({
#     'get': 'user_get_count_api',
# })

# add_user_to_group = UserMVS.as_view({
#     'post': 'add_user_to_group',
# })

# remove_user_from_group = UserMVS.as_view({
#     'delete': 'remove_user_from_group',
# })

# user_get_all_api = UserMVS.as_view({
#     'get': 'user_get_all_api',
# })

# group_get_all_api = UserMVS.as_view({
#     'get': 'group_get_all_api',
# })

# delete_user_api = UserMVS.as_view({
#     'delete':'delete_user_api'
# })

urlpatterns = [
    #
    # path('post/', include('api.post.urls')),
    # path('podcast/', include('api.podcast.urls')),
    # path('try/', include('api.try.urls')),

    #
    path('auth/google/', GoogleView.as_view(), name='google'),
    path('auth/login/', LoginAPIView.as_view(), name='api-login'),
    path('auth/login_admin/', LoginAdminAPIView.as_view(), name='api-login-admin'),
    path('register/', RegisterAPIView.as_view(), name='api-register'),
    # path('user/user_get_list_all_api/', user_get_list_all_api),
    # path('user/user_get_count_api/', user_get_count_api),
    # path('user/add_user_to_group/', add_user_to_group),
    # path('user/remove_user_to_group/', remove_user_from_group),
    # path('user/user_get_all_api/', user_get_all_api),
    # path('group/group_get_all_api/', group_get_all_api),
    path('user/delete_user_api/', UserDeleteAPIView.as_view(), name='delete_user_api'),
]
