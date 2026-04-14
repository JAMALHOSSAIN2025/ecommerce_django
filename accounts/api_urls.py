# 📁 accounts/api_urls.py

from django.urls import path
from .views import (
    RegisterView,
    MyTokenObtainPairView,
    current_user_info,
    user_list_api,
    complete_profile_api,
)
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'accounts_api'

urlpatterns = [
    # JWT Auth Endpoints
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Registration & Profile
    path('register/', RegisterView.as_view(), name='register'),
    path('complete-profile/', complete_profile_api, name='complete_profile_api'),

    # User Info
    path('user/', current_user_info, name='current_user_info'),
    path('users/', user_list_api, name='user_list'),
]
