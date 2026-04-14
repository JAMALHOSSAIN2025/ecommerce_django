# 📁 products/serializers.py

from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True, required=False)

    seller_username = serializers.CharField(source='seller.username', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'seller',
            'seller_username',
            'user',
            'user_username',
            'name',
            'description',
            'price',
            'image',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']
