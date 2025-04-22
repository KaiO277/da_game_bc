from rest_framework import serializers
from api.models import *
from api.submodels import *

class TransactionSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = Transaction
        fields  = '__all__'



