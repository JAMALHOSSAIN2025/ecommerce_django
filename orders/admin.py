from django.contrib import admin
from .models import Order, OrderItem, ShippingAddress

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_price', 'paid', 'is_delivered', 'created_at']
    list_filter = ['paid', 'is_delivered', 'created_at']
    search_fields = ['user__username', 'id']
    inlines = [OrderItemInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'quantity', 'price']

@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'address', 'city', 'postal_code', 'country', 'created_at']
    search_fields = ['user__username', 'address', 'city']
