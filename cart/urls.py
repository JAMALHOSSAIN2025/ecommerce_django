// cart/urls.py

from django.urls import path
from .views import (
    CartView,
    AddToCartView,
    RemoveFromCartView,
    UpdateCartItemView,
    ClearCartView
)

urlpatterns = [
    # 🛒 Get cart
    path('', CartView.as_view(), name='cart-detail'),

    # ➕ Add item
    path('add/', AddToCartView.as_view(), name='cart-add-item'),

    # ✏️ Update quantity
    path('update/<int:item_id>/', UpdateCartItemView.as_view(), name='cart-update-item'),

    # ❌ Remove item
    path('remove/<int:item_id>/', RemoveFromCartView.as_view(), name='cart-remove-item'),

    # 🧹 Clear cart (IMPORTANT for checkout)
    path('clear/', ClearCartView.as_view(), name='cart-clear'),
]