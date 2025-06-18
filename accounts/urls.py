from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    register_view,
    login_view,
    logout_view,
    home_view,
    complete_profile_view,
    user_list_api,
    current_user_info,
    MyTokenObtainPairView,
)

urlpatterns = [
    # UI views
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('home/', home_view, name='home'),
    path('complete-profile/', complete_profile_view, name='complete_profile'),

    # API views
    path('api/users/', user_list_api, name='user_list_api'),
    path('api/me/', current_user_info, name='current_user_info'),

    # JWT token endpoints
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
