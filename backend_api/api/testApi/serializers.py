from rest_framework import serializers
from api.models import *
from api.submodels import *

class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

