from django.shortcuts import render
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q, Count
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from django.forms.models import model_to_dict
import re
from rest_framework.parsers import MultiPartParser, FormParser

from api.models import *
from .serializers import *
from api import status_http

class ProductMVS(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers

    @action(methods=['GET'], detail=False, url_name='product_get_all_api', url_path='product_get_all_api')
    def product_get_all_api(self, request, *args, **kwargs):
        queryset = Product.objects.all()
        serializers = self.serializer_class(queryset, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)
    
    @action(methods=['POST'], detail = False, url_path='product_add_api', url_name='product_add_api')
    def product_add_api(self, request, *args, **kwargs):
        try:
            serializers = self.serializer_class(data=request.data)
            if serializers.is_valid():
                model = serializers.add(request)
                if model:
                    data = {}
                    data['message'] = 'Add successfully!'
                    return Response(data=data, status=status.HTTP_201_CREATED)
                return Response(
                    {'error': 'Duplicate or invalid data'},
                    status=status_http.HTTP_ME_458_DUPLICATE
                )
            return Response(data=serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            print("ProductMVS_add_api: ", error)
        return Response({'error':'Bad request'}, status=status.HTTP_400_BAD_REQUEST)
    
class UserDetailMVS(viewsets.ModelViewSet):
    serializer_class = UserDetailSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Logic tùy chỉnh để lấy dữ liệu
        return User.objects.all()

    @action(methods=['GET'], detail=False, url_path="get_user_detail_api", url_name="get_user_detail_api")
    def get_user_detail_api(self, request, *args, **kwargs):
        """
        API để lấy tất cả thông tin chi tiết của người dùng.
        """
        try:
            # Lấy tất cả các bản ghi từ bảng UserDetail
            queryset = User.objects.all()
            serializer = self.serializer_class(queryset, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            print("UserDetailMVS_get_user_detail_api_error:", error)
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['GET'], detail=False, url_path="get_user_detail_user_id_api", url_name="get_user_detail_user_id_api")
    def get_user_detail_user_id_api(self, request, *args, **kwargs):
        try:
            user_id = kwargs['id']
            if user_id == 0 :
                return Response(data={}, status=status.HTTP_200_OK)
            queryset = User.objects.get(pk=user_id)
            serializer = self.serializer_class(queryset, many=False)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            print("UserDetailMVS_get_by_id_api: ", error)
        return Response({'error':'Bad request'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(methods=['PUT'], detail=False, url_path="update_user_profile_api", url_name="update_user_profile_api")
    def update_user_profile_api(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                updated_user = serializer.update_user_with_profile()
                if updated_user:
                    return Response({'message': 'Cập nhật thành công'}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Lỗi khi cập nhật'}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            print("UserDetailMVS_update_user_profile_api_error:", error)
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)