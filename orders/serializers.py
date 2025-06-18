from rest_framework import serializers
from .models import Order, OrderItem, ShippingAddress
from products.serializers import ProductSerializer


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = ['id', 'address', 'city', 'postal_code', 'country']


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    shipping_address = ShippingAddressSerializer(read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'shipping_address',
            'payment_method',
            'total_price',
            'paid',
            'paid_at',
            'is_delivered',
            'delivered_at',
            'status',
            'order_items',
            'created_at',
        ]
        read_only_fields = ['user', 'paid', 'paid_at', 'is_delivered', 'delivered_at', 'created_at']
