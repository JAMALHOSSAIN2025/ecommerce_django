# order_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_list, name='order-list'),
]
