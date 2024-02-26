from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.views import TokenVerifyView

urlpatterns = [
    path('signup/', views.user, name='user_signup_api'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('login/', TokenObtainPairView.as_view(), name='login_api'),
    path('user_list/', views.user_list, name='user_list_api'),

    path('<int:pk>/', views.user_detail, name='user_detail_api'),
    path('update/', views.update_user_profile, name='update_user_profile_api'),

    # Refactoring URL's after using APIView class
    path('api_view_services/<int:pk>/', views.APIViewUserServices.as_view(), name='user_detail_api_api_view'),
    path('api_view_services/', views.APIViewUserServices.as_view(), name='update_user_profile_api_api_view'),

]
