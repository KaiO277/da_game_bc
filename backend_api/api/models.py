from django.db import models
# from api.submodels.models_post import *
from api.submodels.models_test import *
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.utils import dateformat
import uuid



# Create your models here.
# class CustomUser(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
#     wallet_address = models.CharField(max_length=255, unique=True)
#     avatar_url = models.TextField(null=True, blank=True)
#     role = models.CharField(max_length=50, choices=[('player', 'Player'), ('admin', 'Admin')])
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         # Format birthday to DD-MM-YYYY if it's not None
#         formatted_birthday = dateformat.format(self.birthday, 'd/m/Y') if self.birthday else "N/A"
#         return f"Profile of {self.user.username}, Birthday: {formatted_birthday}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    wallet_address = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        # Format birthday to DD-MM-YYYY if it's not None
        return f"Profile of {self.user.username}, Wallet: {self.wallet_address}"

class SessionToken(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    token = models.CharField(max_length=500, null=True, blank=False)
    hostname = models.CharField(max_length=100, null=True, blank=True)
    ip_address = models.CharField(max_length=100, null=True, blank=True)
    mac_address = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

class Setting(models.Model):
    is_lock_login = models.BooleanField(default=False)

    def __str__(self):
        return "Lock Login: " + str(self.is_lock_login)