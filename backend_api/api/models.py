from django.db import models
# from api.submodels.models_post import *
# from api.submodels.models_podcast import *
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.utils import dateformat

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    birthday = models.DateField(null=True, blank=True)

    def __str__(self):
        # Format birthday to DD-MM-YYYY if it's not None
        formatted_birthday = dateformat.format(self.birthday, 'd/m/Y') if self.birthday else "N/A"
        return f"Profile of {self.user.username}, Birthday: {formatted_birthday}"

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