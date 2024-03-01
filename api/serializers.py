from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from .models import UserProfile, NetworkEdge


class UserCreateSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])  # hash password
        user = User.objects.create(**validated_data)  # create user
        # DETAILS:: User profile will get created when an user instance will get created
        UserProfile.objects.create(user=user)  # create user profile by user instance
        return user

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class UserProfileViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username"]


class UserProfileViewSerializer(serializers.ModelSerializer):
    # user = UserCreateSerializer()
    user = UserProfileViewSerializer()

    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        exclude = ["id", "is_verified"]

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()


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


# Edge Serializers
class NetworkEdgeCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkEdge
        fields = ["from_user", "to_user"]


class NetworkEdgeFollowersViewSerializer(serializers.ModelSerializer):
    from_user = UserProfileViewSerializer()

    class Meta:
        model = NetworkEdge
        fields = ["from_user"]


class NetworkEdgeFollowingViewSerializer(serializers.ModelSerializer):
    to_user = UserProfileViewSerializer()

    class Meta:
        model = NetworkEdge
        fields = ["to_user"]
