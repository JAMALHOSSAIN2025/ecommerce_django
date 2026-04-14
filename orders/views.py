from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from decimal import Decimal

from .models import Order, OrderItem, ShippingAddress
from .serializers import OrderSerializer
from cart.models import Cart


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    user = request.user

    try:
        cart = Cart.objects.get(user=user)
        cart_items = cart.items.all()

        if not cart_items.exists():
            return Response(
                {'detail': 'Cart is empty'},
                status=status.HTTP_400_BAD_REQUEST
            )

        shipping_data = request.data.get('shipping_address', {})

        shipping_address = ShippingAddress.objects.create(
            user=user,
            address=shipping_data.get('address', 'N/A'),
            city=shipping_data.get('city', 'N/A'),
            postal_code=shipping_data.get('postal_code', 'N/A'),
            country=shipping_data.get('country', 'Bangladesh'),
        )

        order = Order.objects.create(
            user=user,
            shipping_address=shipping_address,
            payment_method=request.data.get('payment_method', 'Cash on Delivery'),
            total_price=Decimal('0.00')
        )

        total_price = Decimal('0.00')

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

            total_price += Decimal(str(item.product.price)) * item.quantity

        order.total_price = total_price
        order.save()

        # clear cart safely
        cart.items.all().delete()
        cart.delete()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except Cart.DoesNotExist:
        return Response(
            {'detail': 'Cart not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order_detail(request, pk):
    try:
        order = Order.objects.get(id=pk, user=request.user)
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    except Order.DoesNotExist:
        return Response(
            {'detail': 'Order not found'},
            status=status.HTTP_404_NOT_FOUND
        )