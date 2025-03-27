from django.shortcuts import render
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, action, authentication_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User, Group, Permission
from django.db.models import Q
from collections import OrderedDict
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta, datetime
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth import authenticate

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework.response import Response
import requests, os
from django.http import FileResponse, HttpResponse
from rest_framework_simplejwt.authentication import JWTAuthentication, JWTTokenUserAuthentication
from django.contrib.auth.decorators import login_required
import hashlib
import urllib.parse
from django.contrib.auth.models import Group

from .serializers import *
from . import status_http
from .models import *
from .serializers import RegisterSerializer
from .serializers import UserDeleteSerializer

# Create your views here.

class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Đăng ký thành công"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class UserMVS(viewsets.ModelViewSet):
#     serializer_class = UserSerializer
#     # permission_classes = [IsAuthenticated]

#     @action(methods=['GET'], detail=False, url_name='user_get_list_all_api', url_path='user_get_list_all_api')
#     def user_get_list_all_api(self, request, *args, **kwargs):
#         users = User.objects.all()

#         # Tạo danh sách Users với thông tin nhóm
#         users_data = [
#             {
#                 "id": user.id,
#                 "username": user.username,
#                 "email": user.email,
#                 "groups": [
#                     {"id": group.id, "name": group.name}
#                     for group in user.groups.all()
#                 ]
#             }
#             for user in users
#         ]

#         return Response({"users": users_data}, status=status.HTTP_200_OK)
    
#     @action(methods=['GET'], detail=False, url_name='user_get_all_api', url_path='user_get_all_api')
#     def user_get_all_api(self, request, *args, **kwargs):
#         users = User.objects.filter(groups__isnull=True)  # Đếm số lượng user
#         users_data = [
#             {
#                 "id": user.id,
#                 "username": user.username,
#             }
#             for user in users
#         ]

#         return Response({"users": users_data}, status=status.HTTP_200_OK)
    
#     @action(methods=['GET'], detail=False, url_name='user_get_count_api', url_path='user_get_count_api')
#     def user_get_count_api(self, request, *args, **kwargs):
#         user_count = User.objects.count()  # Đếm số lượng user
#         return Response(
#             {"user_count": user_count}, 
#             status=status.HTTP_200_OK
#         )
    
#     @action(methods=['POST'], detail=False, url_name='add_user_to_group', url_path='add_user_to_group')
#     def add_user_to_group(self, request, *args, **kwargs):
#         # Nhận thông tin từ request
#         user_id = request.data.get('user_id')
#         group_id = request.data.get('group_id')

#         if not user_id or not group_id:
#             return Response({"error": "Both user_id and group_id are required"}, status=status.HTTP_400_BAD_REQUEST)

#         # Kiểm tra người dùng và nhóm có tồn tại không
#         try:
#             user = User.objects.get(id=user_id)
#         except User.DoesNotExist:
#             return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

#         try:
#             group = Group.objects.get(id=group_id)
#         except Group.DoesNotExist:
#             return Response({"error": "Group not found"}, status=status.HTTP_404_NOT_FOUND)

#         # Thêm người dùng vào nhóm
#         user.groups.add(group)
#         # user.save()

#         return Response({"message": f"User {user.username} added to group {group.name}"}, status=status.HTTP_200_OK)

#     @action(methods=['GET'], detail=False, url_name='group_get_all_api', url_path='group_get_all_api')
#     def group_get_all_api(self, request, *args, **kwargs):
#         groups = Group.objects.all()

#         # Serialize group data
#         groups_data = [
#             {
#                 "id": group.id,
#                 "name": group.name,
#             }
#             for group in groups
#         ]

#         return Response({"groups": groups_data}, status=status.HTTP_200_OK)

#     @action(methods=['DELETE'], detail=False, url_name='remove_user_from_group', url_path='remove_user_from_group')
#     def remove_user_from_group(self, request, *args, **kwargs):
#         user_id = request.data.get('user_id')
#         group_id = request.data.get('group_id')

#         if not user_id or not group_id:
#             return Response({"error": "Both user_id and group_id are required"}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             user = User.objects.get(id=user_id)
#         except User.DoesNotExist:
#             return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

#         try:
#             group = Group.objects.get(id=group_id)
#         except Group.DoesNotExist:
#             return Response({"error": "Group not found"}, status=status.HTTP_404_NOT_FOUND)

#         if not user.groups.filter(id=group.id).exists():
#             return Response({"error": f"User {user.username} is not in group {group.name}"}, 
#                             status=status.HTTP_400_BAD_REQUEST)

#         user.groups.remove(group)

#         return Response({"message": f"User {user.username} removed from group {group.name}"}, 
#                         status=status.HTTP_200_OK)

class UserDeleteAPIView(APIView):
    def delete(self, request, *args, **kwargs):
        serializer = UserDeleteSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.delete()
                return Response({'message': 'Deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
            except serializers.ValidationError as error:
                return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GoogleView(APIView):
    def post(self, request):
        # Check if login is locked
        s = Setting.objects.first()
        if s and s.is_lock_login:
            return Response({'message': 'Cannot login at this time'}, status=status.HTTP_403_FORBIDDEN)

        token_google = request.data.get("token_google")
        if not token_google:
            return Response({'message': 'Missing token'}, status=status.HTTP_400_BAD_REQUEST)

        # Verify token with Google
        google_verification_url = f"https://oauth2.googleapis.com/tokeninfo?id_token={token_google}"
        google_response = requests.get(google_verification_url)
        google_data = google_response.json()

        # Handle invalid or expired token
        if google_response.status_code != 200 or 'error' in google_data:
            return Response({'message': 'wrong google token / this google token is already expired.'}, status=status.HTTP_401_UNAUTHORIZED)

        # Extract email from Google's verified data
        email = google_data.get("email")
        if not email:
            return Response({'message': 'Email not found in Google token'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if user exists, otherwise create a new user
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            first_name = google_data.get("given_name", "")
            last_name = google_data.get("family_name", "")
            user = User(
                username=email,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=make_password(BaseUserManager().make_random_password())  # Random password
            )
            user.save()

            # Add user to 'MEMBER' group
            # member_group = Group.objects.get(name=settings.GROUP_NAME['MEMBER'])
            # member_group.user_set.add(user)

        # Generate JWT tokens for the user
        token = RefreshToken.for_user(user)
        return Response({
            'access': str(token.access_token),
            'refresh': str(token)
        }, status=status.HTTP_200_OK)

class LoginAPIView(APIView):
    """
    API đăng nhập cho người dùng, trả về access và refresh token nếu đăng nhập thành công
    """

    def post(self, request):
        # Nhận dữ liệu username và password từ request
        username = request.data.get('username')
        password = request.data.get('password')

        # Xác thực người dùng
        user = authenticate(username=username, password=password)

        if user is not None:
            # Tạo JWT tokens (refresh và access) cho người dùng đã xác thực
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'Sai tên đăng nhập hoặc mật khẩu'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
class LoginAdminAPIView(APIView):
    """
    API đăng nhập cho người dùng, trả về access và refresh token nếu đăng nhập thành công
    """

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Xác thực người dùng
        user = authenticate(username=username, password=password)

        if user is not None:
            # Lấy danh sách các nhóm của user
            user_groups = user.groups.values_list('name', flat=True)

            # Danh sách các nhóm được phép
            allowed_roles = {'superadmin', 'AuthorPost', 'AuthorPodcast'}

            # Kiểm tra nếu user thuộc một trong các nhóm được phép
            if set(user_groups).intersection(allowed_roles):
                # Tạo JWT token
                refresh = RefreshToken.for_user(user)

                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'username': user.username,
                    'roles': list(user_groups),  # Trả về danh sách roles
                }, status=status.HTTP_200_OK)

            # Nếu không thuộc nhóm được phép
            return Response(
                {'error': 'Bạn không có quyền truy cập'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Nếu xác thực thất bại
        return Response(
            {'error': 'Sai thông tin đăng nhập'},
            status=status.HTTP_401_UNAUTHORIZED
        )