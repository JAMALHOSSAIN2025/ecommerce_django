from django.urls import path
from .views import RegisterView, MyTokenObtainPairView, user_list_api, current_user_info

urlpatterns = [
    path('register/', RegisterView.as_view(), name='api-register'),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/', user_list_api, name='user-list'),
    path('me/', current_user_info, name='current-user-info'),
]
