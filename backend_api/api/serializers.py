from django.contrib.auth.models import User, Group, Permission
from django.core.validators import EmailValidator
# from django.db.models import fields
# from django.utils.crypto import get_random_string
# from requests.api import request
from rest_framework import serializers
# from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
import socket
import calendar
import time
from getmac import get_mac_address as gma

from api.models import *


def _token_get_exp(access_token):
    try:
        access_token = AccessToken(access_token)
        return access_token["exp"]
    except Exception as error:
        print("===_token_get_exp", error)
        return None

class ProfileSerializer(serializers.ModelSerializer):
    birthday = serializers.DateField(input_formats=['%d/%m/%Y', '%Y-%m-%d'])

    class Meta:
        model = Profile
        fields = ['birthday']

class RegisterSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()  # Thêm profile vào serializer đăng ký

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'profile']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create_user(**validated_data)
        Profile.objects.create(user=user, **profile_data)
        return user
    
class MySimpleJWTSerializer(TokenObtainPairSerializer):
    my_ip_address = "0.0.0.0"
    myRequest = None


    @classmethod
    def get_token(cls, user):
        # print("user: ", user)
        token = super().get_token(user)
        user_obj = User.objects.get(username=user)
        #
        token["email"] = user_obj.email


        access_token = str(token.access_token)
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        mac_address = gma()
        sessionToken = SessionToken.objects.filter(user=user).count()
        if sessionToken == 0:
            sessionToken = SessionToken.objects.get_or_create(
                user=user,
                token=access_token,
                hostname=hostname,
                ip_address=MySimpleJWTSerializer.my_ip_address,
                mac_address=mac_address,
            )
        else:
            sessionToken = SessionToken.objects.get(user=user)
            token_temp = sessionToken.token
            mac_address_temp = sessionToken.mac_address
            ip_address_temp = sessionToken.ip_address


            #
            exp = _token_get_exp(token_temp)
            if exp is not None:
                ts_now = calendar.timegm(time.gmtime())
                if ts_now < exp:
                    pass
            else:
                SessionToken.objects.filter(user=user).update(
                    token=access_token,
                    hostname=hostname,
                    ip_address=MySimpleJWTSerializer.my_ip_address,
                    mac_address=mac_address,
                )
                print(token)
        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MySimpleJWTSerializer

class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)

    class Meta:
        model = User
        exclude = ['password', 'last_login', 'is_active', 'user_permissions']
 
class UserDeleteSerializer(serializers.Serializer):  # Không sử dụng ModelSerializer
    id = serializers.IntegerField(required=True)  # Chỉ cần trường `id`

    def delete(self):
        try:
            user_id = self.validated_data['id']
            user = User.objects.get(pk=user_id)
            user.delete()
            return True
        except User.DoesNotExist:
            raise serializers.ValidationError({'error': f"User with id {user_id} does not exist."})
        except Exception as error:
            raise serializers.ValidationError({'error': 'An unexpected error occurred.'})