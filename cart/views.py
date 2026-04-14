from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from .models import Cart, CartItem
from products.models import Product
from .serializers import CartSerializer, CartItemSerializer


# 🟢 GET CART
class CartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


# 🟢 ADD TO CART
class AddToCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {'error': 'Product not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        cart, _ = Cart.objects.get_or_create(user=request.user)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product
        )

        if created:
            cart_item.quantity = quantity
        else:
            cart_item.quantity += quantity

        cart_item.save()

        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)


# 🟡 UPDATE ITEM (SET EXACT QUANTITY)
class UpdateCartItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, item_id):
        quantity = int(request.data.get('quantity', 1))

        if quantity < 1:
            return Response(
                {'error': 'Quantity must be at least 1'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            cart_item = CartItem.objects.get(
                id=item_id,
                cart__user=request.user
            )

            cart_item.quantity = quantity
            cart_item.save()

            serializer = CartItemSerializer(cart_item)
            return Response(serializer.data)

        except CartItem.DoesNotExist:
            return Response(
                {'error': 'Item not found'},
                status=status.HTTP_404_NOT_FOUND
            )


# ❌ REMOVE SINGLE ITEM
class RemoveFromCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, item_id):
        try:
            cart_item = CartItem.objects.get(
                id=item_id,
                cart__user=request.user
            )

            cart_item.delete()

            return Response(
                {'message': 'Item removed'},
                status=status.HTTP_204_NO_CONTENT
            )

        except CartItem.DoesNotExist:
            return Response(
                {'error': 'Item not found'},
                status=status.HTTP_404_NOT_FOUND
            )


# 🧹 CLEAR CART (NEW - IMPORTANT FOR CHECKOUT)
class ClearCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart.items.all().delete()

        return Response(
            {'message': 'Cart cleared successfully'},
            status=status.HTTP_200_OK
        )