from django.urls import path
from . import views

urlpatterns = [
    path('', views.CartView.as_view(), name='cart-detail'),  # GET, POST cart details
    path('add/', views.AddToCartView.as_view(), name='cart-add-item'),  # POST add item
    path('remove/<int:item_id>/', views.RemoveFromCartView.as_view(), name='cart-remove-item'),  # DELETE item
    path('update/<int:item_id>/', views.UpdateCartItemView.as_view(), name='cart-update-item'),  # PATCH update qty
]
