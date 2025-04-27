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

from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import Profile
from solders.pubkey import Pubkey
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
from base64 import b64decode
import time

@api_view(['POST'])
def login(request):
    """
    API đăng nhập bằng cách xác thực chữ ký Solana và trả về JWT token.
    Request body:
    - wallet_address: địa chỉ ví người dùng (string)
    - signature: chữ ký đã được base64 mã hóa (string)
    - message: thông điệp cần xác thực chữ ký (string)
    """
    try:
        # Lấy dữ liệu từ request
        wallet_address = request.data.get('wallet_address')
        signature = request.data.get('signature')
        message = request.data.get('message')

        # Kiểm tra các trường cần thiết có được cung cấp hay không
        if not wallet_address or not signature or not message:
            return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

        # Kiểm tra tính hợp lệ của thông điệp (timestamp không quá 60 giây)
        # if not is_message_fresh(message):
        #     return Response({"error": "Expired message"}, status=status.HTTP_400_BAD_REQUEST)

        # Xác thực chữ ký
        pubkey_bytes = bytes(Pubkey.from_string(wallet_address))  # Chuyển wallet_address thành bytes
        verify_key = VerifyKey(pubkey_bytes)
        signature_bytes = b64decode(signature)
        verify_key.verify(message.encode(), signature_bytes)  # Kiểm tra chữ ký

        # Nếu không có lỗi, lấy hoặc tạo User
        user, created = User.objects.get_or_create(username=wallet_address)

        # Tạo JWT token
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({
            "message": "Login successful",
            "username": user.username,
            "access_token": access_token  # Trả về access token
        }, status=status.HTTP_200_OK)

    except BadSignatureError:
        return Response({"error": "Invalid signature"}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def check_username_exists(request):
    """
    API kiểm tra xem username có tồn tại trong cơ sở dữ liệu hay không.
    Query parameter:
    - username: tên người dùng cần kiểm tra
    """
    username = request.query_params.get('username')
    if not username:
        return Response({"error": "Missing 'username' parameter"}, status=status.HTTP_400_BAD_REQUEST)

    exists = User.objects.filter(username=username).exists()
    return Response({"username": username, "exists": exists}, status=status.HTTP_200_OK)

@api_view(['POST'])
def register_or_login_wallet(request):
    """
    API đăng ký hoặc đăng nhập người dùng bằng cách xác thực chữ ký và trả về token JWT.
    """
    try:
        username = request.data.get('username')
        profile_data = request.data.get('profile', {})
        wallet_address = profile_data.get('wallet_address')
        signature = profile_data.get('signature')
        message = profile_data.get('message')

        if not username or not wallet_address or not signature or not message:
            return Response({"error": "Missing fields"}, status=status.HTTP_400_BAD_REQUEST)

        # Kiểm tra tính hợp lệ của chữ ký
        pubkey_bytes = bytes(Pubkey.from_string(wallet_address))
        verify_key = VerifyKey(pubkey_bytes)
        signature_bytes = b64decode(signature)
        verify_key.verify(message.encode(), signature_bytes)

        # Nếu chữ ký hợp lệ, tạo hoặc lấy User
        user, created = User.objects.get_or_create(username=username)
        
        # Tạo profile cho người dùng
        profile, _ = Profile.objects.get_or_create(user=user)
        profile.wallet_address = wallet_address
        profile.save()

        # Tạo JWT token cho người dùng
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({
            "message": "Login/Register successful",
            "username": user.username,
            "wallet": profile.wallet_address,
            "access_token": access_token  # Trả về JWT token
        }, status=status.HTTP_200_OK)

    except BadSignatureError:
        return Response({"error": "Invalid signature"}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
def is_message_fresh(message: str) -> bool:
    """
    Kiểm tra xem message có bị quá hạn (cũ hơn 60s) hay không.
    Format: "Sign to register Meme Runner at 2025-04-20T16:01:00Z"
    """
    try:
        parts = message.strip().split(" at ")
        if len(parts) != 2:
            return False
        timestamp_str = parts[1]
        msg_time = time.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%SZ")
        msg_timestamp = calendar.timegm(msg_time)  # ✅ đổi mktime -> timegm
        now = time.time()
        return abs(now - msg_timestamp) < 60
    except Exception as e:
        print("DEBUG is_message_fresh:", str(e))
        return False

def index(request):
    return HttpResponse("<h1>Trang Index - Test Django trên Railway</h1>")

class RegisterAPIView(APIView):
    def post(self, request):
        try:
            serializer = RegisterSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                return Response({
                    "message": "Đăng ký thành công",
                    "user_id": str(user.id),
                    "username": user.username,
                    "wallet_address": user.profile.wallet_address,
                    "role": user.profile.role
                }, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            import traceback
            traceback.print_exc()  # hoặc log bằng logger nếu bạn dùng log framework
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserMeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

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