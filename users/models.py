from django.db import models


# Create your models here.
class Users(models.Model):
    # work as a primary key
    # id =models.AutoField(primary_key=True)

    username = models.CharField(max_length=50, unique=True, blank=False, null=False)
    email = models.EmailField(max_length=50, unique=True, blank=False, null=False)
    password = models.CharField(max_length=15, blank=False, null=False)
    phone = models.CharField(max_length=10, unique=True, blank=False, null=False)

    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class UserProfile(models.Model):
    # id =models.AutoField(primary_key=True)

    DEFAULT_PROFILE_PICTURE_URL = 'https://placehold.jp/3d4070/ffffff/150x150.png'
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=False)
    profile_picture = models.CharField(max_length=255, default=DEFAULT_PROFILE_PICTURE_URL)

    bio = models.CharField(max_length=25, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
