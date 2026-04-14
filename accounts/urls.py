# 📁 accounts/urls.py

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    # UI Views
    register_view,
    login_view,
    logout_view,
    home_view,
    complete_profile_view,

    # API Views
    MyTokenObtainPairView,
    RegisterView,
    user_list_api,
    current_user_info,
    complete_profile_api,
)

app_name = 'accounts'

urlpatterns = [
    # ---------- UI Views ----------
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('home/', home_view, name='home'),
    path('complete-profile/', complete_profile_view, name='complete_profile'),

    # ---------- API (JWT Auth & Profile) ----------
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterView.as_view(), name='api_register'),
    path('api/complete-profile/', complete_profile_api, name='complete_profile_api'),
    path('api/users/', user_list_api, name='user_list_api'),
    path('api/user/', current_user_info, name='current_user_info'),
]
