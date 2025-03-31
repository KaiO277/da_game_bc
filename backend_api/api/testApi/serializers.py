from rest_framework import serializers
from api.models import *
from api.submodels import *

class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def add(self,request):
        try:
            name = self.validated_data['name']
            price = self.validated_data['price']
            description = self.validated_data['description']

            if Product.objects.filter(name=name).exists():
                print("ProductSerializers_add_error: Dulicate title")
                return None 

            return Product.objects.create(
                name=name,
                price=price,
                description=description
            )
        except Exception as error:
            print("ProductSerializer_add_error: ", error)
            return None