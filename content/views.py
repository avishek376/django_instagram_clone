from django.shortcuts import render

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import UserPostCreateSerializer, PostMediaCreateSerializer
from rest_framework import generics
from .models import UserPost, PostMedia
from rest_framework import mixins


# Create your views here.

# DETAILS:: CREATE the post with the author-id,
#  upload the media files with the reference of the post-id in the last-step,
#  update the post & publish

class UserPostCreateFeed(generics.GenericAPIView,
                         mixins.CreateModelMixin):
    queryset = UserPost.objects.all()
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [JWTAuthentication, ]
    serializer_class = UserPostCreateSerializer

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
                                mixins.UpdateModelMixin):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [JWTAuthentication, ]
    serializer_class = UserPostCreateSerializer
    queryset = UserPost.objects.all()

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
