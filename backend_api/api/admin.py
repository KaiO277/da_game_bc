from django.contrib import admin
from django.contrib.auth.models import User
from .submodels.models_test import *


# Register your models here.

admin.site.register(User)
admin.site.register(NFT)
admin.site.register(Product)
admin.site.register(Race)
admin.site.register(Bet)
admin.site.register(Transaction)


