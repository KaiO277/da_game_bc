from rest_framework import serializers
from api.models import *
from api.submodels import *

class NTFSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = NFT
        fields  = '__all__'

    def add(self, request):
        try:
            name = self.validated_data['name']
            token_id = self.validated_data['token_id']
            image_url = self.validated_data['image_url']
            user = self.validated_data['user']  # vẫn giữ user từ validated_data

            return NFT.objects.create(
                name=name,
                token_id=token_id,
                image_url=image_url,
                staked=False,  # ✅ mặc định là False
                user=user
            )
        except Exception as error:
            print("NTFSerializer_add_error: ", error)
            return None
        
    def isStake(self):
        try:
            id = self.validated_data['id']
            nft = NFT.objects.get(pk=id)
            nft.staked = True
            nft.save()
            return nft
        except NFT.DoesNotExist:
            print("NFTStakeSerializer_update_stake_error: NFT not found")
            return None
        except Exception as error:
            print("NFTStakeSerializer_update_stake_error:", error)
            return None
    
    def delete(self, request):
        try:
            id = self.validated_data['id']
            nft = NFT.objects.get(pk=id)
            nft.delete()
            return True
        except NFT.DoesNotExist:
            print("NFTStakeSerializer_delete_error: NFT not found")
            return False
        except Exception as error:
            print("NFTStakeSerializer_delete_error:", error)
            return False