from django.shortcuts import render

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import UserPostCreateSerializer, PostMediaCreateSerializer, PostFeedSerializer
from rest_framework import generics
from .models import UserPost, PostMedia
from rest_framework import mixins
from .filters import CurrentUserFollowingFilterBackend


# Create your views here.

# DETAILS:: CREATE the post with the author-id,
#  upload the media files with the reference of the post-id in the last-step,
#  update the post & publish

class UserPostCreateFeed(generics.GenericAPIView,
                         mixins.ListModelMixin,
                         mixins.CreateModelMixin):
    queryset = UserPost.objects.all()
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [JWTAuthentication, ]
    serializer_class = UserPostCreateSerializer
    filter_backends = [CurrentUserFollowingFilterBackend, ]

    # TODO:: Create a system to follow topics or hashtags
    # TODO: Create a way of ordering the feed based on post popularity

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostFeedSerializer
        return self.serializer_class

    def get_serializer_context(self):
        return {'current_user': self.request.user.profile}

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PostMediaView(generics.GenericAPIView,
                    mixins.CreateModelMixin):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [JWTAuthentication, ]
    serializer_class = PostMediaCreateSerializer

    # for using create we will have to import mixins.CreateModelMixin
    # should be made idempotent
    def put(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class UserPostDetailsUpdateView(generics.GenericAPIView,
                                mixins.RetrieveModelMixin,
                                mixins.UpdateModelMixin):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [JWTAuthentication, ]
    serializer_class = UserPostCreateSerializer
    queryset = UserPost.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostFeedSerializer
        return self.serializer_class

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
