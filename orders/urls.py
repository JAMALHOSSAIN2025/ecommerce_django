from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_order, name='create-order'),
    path('my-orders/', views.get_my_orders, name='my-orders'),
    path('<int:pk>/', views.get_order_detail, name='order-detail'),
]
