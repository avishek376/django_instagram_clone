from rest_framework.serializers import ModelSerializer
from .models import UserPost, PostMedia


class UserPostCreateSerializer(ModelSerializer):

    def create(self, validated_data):
        validated_data['author'] = self.context['current_user']
        return UserPost.objects.create(**validated_data)

    class Meta:
        model = UserPost
        fields = ['caption_text', 'location', 'id', 'is_published']


class PostMediaCreateSerializer(ModelSerializer):
    class Meta:
        model = PostMedia
        fields = ['media_file', 'sequence_index', 'post']
