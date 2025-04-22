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
            race = Race.objects.filter(pk=id)
            serializer = self.get_serializer(race, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            print("RaceMVS_get_race_by_id_api: ", error)
        return Response({'error':'Bad request'}, status=status.HTTP_400_BAD_REQUEST)


    
