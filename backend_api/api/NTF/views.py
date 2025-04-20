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

class NTFsMVS(viewsets.ModelViewSet):
    serializer_class = NTFSerializers
    token_id = serializers.CharField()

    @action(methods=['GET'], detail=False, url_path="get_ntfs_by_user_id_api", url_name="get_ntfs_by_user_id_api")
    def get_ntfs_by_user_id_api(self, request, *args,  ** kwargs):
        try:
            user_id = request.data.get('user_id')
            if user_id == 0:
                return Response(data={}, status=status.HTTP_200_OK)
            nfts = NFT.objects.filter(user__id=user_id)
            serializer = self.get_serializer(nfts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            print("NTFsMVS_get_ntfs_by_user_id_api: ", error)
        return Response({'error':'Bad request'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(methods=['GET'], detail=False, url_path="get_ntfs_by_id_api", url_name="get_ntfs_by_id_api")
    def get_ntfs_by_id_api(self, request, *args,  ** kwargs):
        try:
            id = kwargs['id']
            if id == 0:
                return Response(data={}, status=status.HTTP_200_OK)
            nfts = NFT.objects.filter(pk=id)
            serializer = self.get_serializer(nfts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            print("NTFsMVS_get_ntfs_by_id_api: ", error)
        return Response({'error':'Bad request'}, status=status.HTTP_400_BAD_REQUEST)
    

    @action(methods=['POST'], detail=False, url_path='add_ntfs_api', url_name='add_ntfs_api')
    def add_ntfs_api(self, request, *args, **kwargs):
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
            print("NTFsMVS_add_ntfs_api: ", error)
        return Response({'error':'Bad request'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(methods=['PUT'], detail=False, url_path='update_staked_api', url_name='update_staked_api')
    def update_staked_api(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data, partial=True)  # ✅ thêm partial=True
            if serializer.is_valid():
                nft = serializer.isStake()  # đừng quên gọi hàm `isStake()`, không phải `isStake`
                if nft:
                    return Response({'message': 'Staked successfully!'}, status=status.HTTP_200_OK)
                return Response({'error': 'NFT not found'}, status=status.HTTP_404_NOT_FOUND)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            print("NTFsMVS_update_staked_api_error: ", error)
            return Response({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)
