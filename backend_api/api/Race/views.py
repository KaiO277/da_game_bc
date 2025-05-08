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

class RaceMVS(viewsets.ModelViewSet):
    serializer_class = RaceSerializers
   
    def get_queryset(self):
        return Race.objects.all()

    @action(methods=['GET'], detail=False, url_path = 'get_all_race_api', url_name = 'get_all_race_api')
    def get_all_race_api(self, request, *args, **kwargs):
        try:
            queryset = Race.objects.all()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            print("RaceMVS_get_all_race_api: ", error)
        return Response({'error':'Bad request'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(methods=['GET'], detail=False, url_path ='get_race_by_id_api', url_name='get_race_by_id_api')
    def get_race_by_id_api(self, request, *args, **kwargs):
        try:
            id = kwargs['id']
            if id == 0:
                return Response(data={}, status=status.HTTP_200_OK)
            race = Race.objects.filter(pk=id).first() 
            serializer = self.serializer_class(race, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            print("RaceMVS_get_race_by_id_api: ", error)
        return Response({'error':'Bad request'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(methods=['POST'], detail=False, url_path='add_race_api', url_name='add_race_api')
    def add_race_api(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                model = serializer.add(request)
                if model:
                    data = {}
                    data['message'] = 'Add successfully!'
                    return Response(data=data, status=status.HTTP_201_CREATED)
                return Response(
                    {'error': 'Duplicate or invalid data'},
                    status=status_http.HTTP_ME_458_DUPLICATE
                )
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            print("RaceMVS_add_race_api: ", error)
        return Response({'error':'Bad request'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(methods=['PUT'], detail=True, url_path='update_race_status_api', url_name='update_race_status_api')
    def update_race_status_api(self, request, pk=None, *args, **kwargs):
        """
        API để cập nhật các trường status, end_time, và winner_nft của Race.
        """
        try:
            # Lấy Race từ pk (id) trong URL
            try:
                race = Race.objects.get(pk=pk)
            except Race.DoesNotExist:
                return Response({"error": "Race not found"}, status=status.HTTP_404_NOT_FOUND)

            # Lấy dữ liệu cần cập nhật từ request
            status_value = request.data.get('status')
            end_time_value = request.data.get('end_time')
            winner_nft_id = request.data.get('winner_nft')

            # Cập nhật các trường nếu có trong request
            if status_value:
                race.status = status_value
            if end_time_value:
                race.end_time = end_time_value
            if winner_nft_id:
                try:
                    winner_nft = NFT.objects.get(pk=winner_nft_id)
                    race.winner_nft = winner_nft
                except NFT.DoesNotExist:
                    return Response({"error": "Winner NFT not found"}, status=status.HTTP_404_NOT_FOUND)

            # Lưu thay đổi
            race.save()

            # Trả về thông tin Race đã cập nhật
            serializer = self.get_serializer(race)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as error:
            print("RaceMVS_update_race_status_api_error: ", error)
            return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['DELETE'], detail=True, url_path='delete_race_api', url_name='delete_race_api')
    def delete_race_api(self, request, pk=None, *args, **kwargs):
        try:    
            id = kwargs.get('id')
            if not id:
                return Response(data={}, status=status.HTTP_400_BAD_REQUEST)
            
            Race.objects.filter(pk=id).delete()
            return Response(data={'message': 'Delete successfully!'}, status=status.HTTP_200_OK)
        except Exception as error:
            print("RaceMVS_delete_race_api_error:", error)
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)