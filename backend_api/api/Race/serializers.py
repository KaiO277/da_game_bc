from rest_framework import serializers
from api.models import *
from api.submodels import *

class RaceSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = Race
        fields  = '__all__'

    def add(self, request):
        try:
            name = self.validated_data['name']
            status = self.validated_data['status']
            start_time = self.validated_data['start_time']
            end_time = self.validated_data['end_time']
            winner_nft = self.validated_data['winner_nft']  # vẫn giữ winner_nft từ validated_data
        
            return Race.objects.create(
                name=name,
                status=status,
                start_time=start_time,
                end_time=end_time,
                winner_nft=winner_nft
            )
        except Exception as error:
            print("RaceSerializer_add_error: ", error)
            return None