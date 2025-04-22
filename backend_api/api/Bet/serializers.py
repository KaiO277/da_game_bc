from rest_framework import serializers
from api.models import *
from api.submodels import *

class BetSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = Bet
        fields  = '__all__'

    def add(self, request):
        try:
            user = self.validated_data['user']
            nft = self.validated_data['nft']
            race = self.validated_data['race']
            amount = self.validated_data['amount']

            return Bet.objects.create(
                user=user,
                nft=nft,
                race = race,
                amount=amount
            )

        except Exception as error:
            print("BetSerializer_add_error: ", error)
            return None

