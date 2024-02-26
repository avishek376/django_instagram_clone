from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from .models import UserProfile


class UserCreateSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])  # hash password
        user = User.objects.create(**validated_data)  # create user
        UserProfile.objects.create(user=user)  # create user profile by user instance
        return user

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class UserProfileViewSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer()

    class Meta:
        model = UserProfile
        exclude = ["id", "is_verified"]


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    def update(self, instance, validated_data):
        """Update the user profile"""
        user = instance.user
        user.first_name = validated_data.pop('first_name', None)
        user.last_name = validated_data.pop('last_name', None)
        user.save()
        instance.bio = validated_data.get('bio', None)
        instance.profile_picture = validated_data.get('profile_picture', None)
        instance.save()
        return instance

    class Meta:
        model = UserProfile
        fields = ["first_name", "last_name", "bio", "profile_picture"]
