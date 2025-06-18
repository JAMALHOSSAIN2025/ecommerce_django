# products/urls.py

from django.urls import path
from . import views
from .api_views import product_list_api

urlpatterns = [
    path('', views.product_list, name='product_list'),  # HTML template view
    path('add/', views.add_product, name='add_product'),  # HTML template view
    path('api/', product_list_api, name='product_list_api'),  # ✅ React এর জন্য JSON API
]
