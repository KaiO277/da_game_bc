from rest_framework import serializers
from api.models import *
from api.submodels import *
from api.serializers import ProfileSerializer

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
        
class UserDetailSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile']

    def update_user_with_profile(self):
        try:
            user_id = self.validated_data['id']
            username = self.validated_data.get('username')
            first_name = self.validated_data.get('first_name')
            last_name = self.validated_data.get('last_name')
            email = self.validated_data.get('email')
            password = self.validated_data.get('password')

            profile_data = self.validated_data.get('profile', {})
            wallet_address = profile_data.get('wallet_address')
            avatar_url = profile_data.get('avatar_url')
            role = profile_data.get('role')
            birthday = profile_data.get('birthday')

            user = User.objects.get(pk=user_id)

            # Update User fields
            if username: user.username = username
            if first_name: user.first_name = first_name
            if last_name: user.last_name = last_name
            if email: user.email = email
            if password: user.set_password(password)
            user.save()

            # Update Profile fields
            profile = user.profile
            if wallet_address: profile.wallet_address = wallet_address
            if avatar_url: profile.avatar_url = avatar_url
            if role: profile.role = role
            if birthday: profile.birthday = birthday
            profile.save()

            return user

        except Exception as error:
            print("UserProfileUpdateSerializer_update_user_with_profile_error:", error)
            return None