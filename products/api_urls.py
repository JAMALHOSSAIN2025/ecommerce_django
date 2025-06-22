

from django.urls import path
from .api_views import product_list_api

urlpatterns = [
    path('', product_list_api, name='product_list_api'),
]
