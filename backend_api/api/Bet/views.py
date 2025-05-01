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

class BetMVS(viewsets.ModelViewSet):
    serializer_class = BetSerializers

    def get_queryset(self):
        # Logic tùy chỉnh để lấy dữ liệu
        return Bet.objects.all()

    @action(methods=['GET'], detail=False, url_path = 'get_all_bet_api', url_name = 'get_all_bet_api')
    def get_all_bet_api(self, request, *args, **kwargs):
        try:
            queryset = Bet.objects.all()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            print("BetMVS_get_all_bet_api: ", error)
        return Response({'error':'Bad request'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(methods=['GET'], detail=False, url_path ='get_bet_by_id_api', url_name='get_bet_by_id_api')
    def get_bet_by_id_api(self, request, *args, **kwargs):
        try:
            id = kwargs['id']
            if id == 0:
                return Response(data={}, status=status.HTTP_200_OK)
            bet = Bet.objects.filter(pk=id)
            serializer = self.get_serializer(bet, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            print("BetMVS_get_bet_by_id_api: ", error)
        return Response({'error':'Bad request'}, status=status.HTTP_400_BAD_REQUEST)

    # @action(methods=['POST'], detail=False, url_path ='add_bet_api', url_name='add_bet_api')
    # def add_bet_api(self, request, *args, **kwargs):
    #     try:
    #         serializer = self.get_serializer(data=request.data)
    #         if serializer.is_valid():
    #             bet = serializer.add(request)
    #             if bet:
    #                 return Response(serializer.data, status=status.HTTP_201_CREATED)
    #             else:
    #                 return Response({'error':'Bad request'}, status=status.HTTP_400_BAD_REQUEST)
    #         else:
    #             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     except Exception as error:
    #         print("BetMVS_add_bet_api: ", error)
    #     return Response({'error':'Bad request'}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=False, url_path='add_bet_api', url_name='add_bet_api')
    def add_bet_api(self, request, *args, **kwargs):
        """
        API thêm một bản ghi Bet.
        Input:
        {
            "nft_id": 1,
            "wallet_address": "0xABCDEF123456",
            "race_id": 1,
            "amount": 2
        }
        """
        try:
            # Lấy dữ liệu từ request
            wallet_address = request.data.get('wallet_address')
            nft_id = request.data.get('nft_id')
            race_id = request.data.get('race_id')
            amount = request.data.get('amount')

            # Kiểm tra các trường cần thiết
            if not wallet_address or not nft_id or not race_id or not amount:
                return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

            # Lấy user từ wallet_address thông qua bảng Profile
            try:
                profile = Profile.objects.get(wallet_address=wallet_address)
                user_id = profile.user.id  # Lấy ID của User
                print("user_id: ", user_id)
            except Profile.DoesNotExist:
                return Response({"error": "Wallet address not registered"}, status=status.HTTP_404_NOT_FOUND)

            # Lấy NFT từ nft_id
            try:
                nft = NFT.objects.get(pk=nft_id)
                nft_id = nft.id  # Lấy ID của NFT
            except NFT.DoesNotExist:
                return Response({"error": "NFT not found"}, status=status.HTTP_404_NOT_FOUND)

            # Lấy Race từ race_id
            try:
                race = Race.objects.get(pk=race_id)
                race_id = race.id  # Lấy ID của Race
            except Race.DoesNotExist:
                return Response({"error": "Race not found"}, status=status.HTTP_404_NOT_FOUND)

            # Chuẩn bị dữ liệu để thêm Bet
            bet_data = {
                "user": user_id,  # Truyền ID thay vì đối tượng User
                "nft": nft_id,    # Truyền ID thay vì đối tượng NFT
                "race": race_id,  # Truyền ID thay vì đối tượng Race
                "amount": amount
            }

            # Sử dụng hàm add trong serializer để tạo Bet
            serializer = self.get_serializer(data=bet_data)
            if serializer.is_valid():
                bet = serializer.add(request)
                if bet:
                    return Response({"message": "Bet created successfully", "bet_id": bet.id}, status=status.HTTP_201_CREATED)
                else:
                    return Response({"error": "Failed to create Bet"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as error:
            print("BetMVS_add_bet_api_error: ", error)
            return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)