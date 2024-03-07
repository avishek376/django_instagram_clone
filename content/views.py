from django.shortcuts import render

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import UserPostCreateSerializer, PostMediaCreateSerializer, \
    PostFeedSerializer, \
    PostLikeSerializer, \
    PostCommentSerializer
from rest_framework import generics
from .models import UserPost, PostMedia, PostLikes, PostComments
from rest_framework import mixins
from .filters import CurrentUserFollowingFilterBackend
from rest_framework import viewsets

from rest_framework.response import Response
from .permissions import IsOwnerOrReadOnly


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


# DETAILS:: If we implement
#  1)ViewSet...urls get configured automatically but
#  the methods needs to implemented for HTTP verbs to work
#  2)GenericViewSet...add mixins,
#  also has the methods like get_serializer_class, get_serializer_context
#  3)ModelViewSet...urls + methods are already implemented

class PostLikeViewSet(mixins.DestroyModelMixin,
                      mixins.CreateModelMixin,
                      viewsets.GenericViewSet):
    queryset = PostLikes.objects.all()
    serializer_class = PostLikeSerializer
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [JWTAuthentication, ]

    def get_serializer_context(self):
        return {'current_user': self.request.user.profile}

    def list(self, request):
        post_likes = self.queryset.filter(post_id=request.query_params['post_id'])
        page = self.paginate_queryset(post_likes)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(post_likes, many=True)

        return Response(serializer.data)


class PostCommentViewSet(mixins.ListModelMixin,
                         mixins.DestroyModelMixin,
                         mixins.CreateModelMixin,
                         viewsets.GenericViewSet):
    queryset = PostComments.objects.all()
    serializer_class = PostCommentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly, ]
    authentication_classes = [JWTAuthentication, ]

    def get_serializer_context(self):
        return {'current_user': self.request.user.profile}

    def list(self, request):
        # TODO:: Implement get_serializer_class
        #  to have a proper representation for the user' profile

        post_comments = self.queryset.filter(post_id=request.query_params['post_id'])
        page = self.paginate_queryset(post_comments)

        if page:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(post_comments, many=True)
        return Response(serializer.data)
