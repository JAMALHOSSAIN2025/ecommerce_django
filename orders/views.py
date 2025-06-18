from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

from .models import Order, OrderItem, ShippingAddress
from .serializers import OrderSerializer
from products.models import Product


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    user = request.user
    data = request.data

    # Get Cart Items
    items = data.get('order_items', [])
    if not items:
        return Response({'detail': 'No order items provided'}, status=status.HTTP_400_BAD_REQUEST)

    # Create shipping address
    shipping = data.get('shipping_address', {})
    shipping_address = ShippingAddress.objects.create(
        user=user,
        address=shipping.get('address'),
        city=shipping.get('city'),
        postal_code=shipping.get('postal_code'),
        country=shipping.get('country'),
    )

    # Create order
    order = Order.objects.create(
        user=user,
        shipping_address=shipping_address,
        payment_method=data.get('payment_method', 'Cash on Delivery'),
        total_price=data.get('total_price', 0.00)
    )

    # Create order items
    for item in items:
        product_id = item['product']
        quantity = item['quantity']
        product = Product.objects.get(id=product_id)

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=product.price,
        )

    serializer = OrderSerializer(order, many=False)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


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
        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)
    except Order.DoesNotExist:
        return Response({'detail': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
