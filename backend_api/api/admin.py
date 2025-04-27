from django.contrib import admin
from .models import Profile, NFT, Product
from .submodels.models_test import *


# Register your models here.

admin.site.register(Profile)
admin.site.register(NFT)
admin.site.register(Product)
admin.site.register(Race)
admin.site.register(Bet)
admin.site.register(Transaction)


