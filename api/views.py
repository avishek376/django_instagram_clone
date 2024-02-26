from django.shortcuts import render
from .models import UserProfile
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .serializers import UserCreateSerializer, UserProfileViewSerializer, UserProfileUpdateSerializer
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView


# Create your views here.

@api_view(['POST'])
def user(request):
    data = request.data
    serializer = UserCreateSerializer(data=data)
    response_data = {
        "message": None,
        "data": None,
        "errors": None
    }
    if serializer.is_valid():
        user_data = serializer.save()  # save user
        refresh = RefreshToken.for_user(user_data)  # generate token
        response_data["message"] = "User created successfully"

        # generating access and refresh token by user instance
        response_data["data"] = {  # return token
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        response_status = status.HTTP_201_CREATED
    else:
        response_data["errors"] = serializer.errors
        response_status = status.HTTP_400_BAD_REQUEST
    return Response(response_data, status=response_status)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def user_list(request):
    # print("Request User ==> ", request.user)
    users = UserProfile.objects.all()
    # We have existent data that we have to send back through API..for that we use instance attribute
    # and set many=True because we have multiple data
    serialized_data = UserProfileViewSerializer(instance=users, many=True)
    return Response(serialized_data.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def user_detail(request, pk=None):
    user = UserProfile.objects.filter(id=pk).first()
    # data = request.data()

    response_data = {
        "data": None,
        "errors": None,
    }
    if user:
        serialized_data = UserProfileViewSerializer(instance=user)
        response_data["data"] = serialized_data.data
        response_status = status.HTTP_200_OK
    else:
        response_data["errors"] = "User not found"
        response_status = status.HTTP_404_NOT_FOUND
    return Response(response_data, status=response_status)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_user_profile(request):
    serializer = UserProfileUpdateSerializer(instance=request.user.profile, data=request.data)

    response_data = {
        "message": None,
        "data": None,
        "errors": None,
    }
    if serializer.is_valid():
        user_profile = serializer.save()
        response_data["data"] = UserProfileViewSerializer(instance=user_profile).data
        response_data["message"] = "User profile updated successfully"
        response_status = status.HTTP_200_OK
    else:
        response_data["errors"] = serializer.errors
        response_status = status.HTTP_400_BAD_REQUEST
    return Response(response_data, status=response_status)


# Refactoring the user_detail function by using APIView class
class APIViewUserServices(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = UserProfileViewSerializer

    # TODO:: Refactoring the user_detail by ID function by using APIView class
    def get(self, request, pk=None):
        print("line no:", 117)
        user = UserProfile.objects.filter(id=pk).first()
        # print("User ==> ", user)
        response_data = {
            "data": None,
            "errors": None,
        }
        if user:
            serializer = UserProfileViewSerializer(instance=user)
            response_data["data"] = serializer.data
            response_status = status.HTTP_200_OK
        else:
            response_data["errors"] = "User not found"
            response_status = status.HTTP_404_NOT_FOUND
        return Response(response_data, status=response_status)

    # TODO:: Refactoring the update_user_profile function by using APIView class
    def post(self, request):
        user = UserProfileUpdateSerializer(instance=request.user.profile, data=request.data)
        response_data = {
            "message": None,
            "data": None,
            "errors": None,
        }

        if user.is_valid():
            user_profile = user.save()
            response_data["message"] = "User profile updated successfully"
            response_data["data"] = UserProfileViewSerializer(instance=user_profile).data
            response_status = status.HTTP_200_OK
        else:
            response_data["errors"] = user.errors
            response_status = status.HTTP_400_BAD_REQUEST
        return Response(response_data, status=response_status)


class APIViewUserListService(APIView):
    serializer_class = UserProfileViewSerializer
    permission_classes = ['IsAuthenticated']
    authentication_classes = ['JWTAuthentication']

    def get(self, request):
        users = UserProfile.objects.all()
        serialized_data = UserProfileViewSerializer(instance=users, many=True)
        print("line no: ", 149)
        return Response(serialized_data.data, status=status.HTTP_200_OK)

# TODO:: Refactoring the user_list function by using Mixins
