from django.contrib import admin
from .models import Order, OrderItem

# Order Admin
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_price', 'created_at', 'updated_at', 'wishlist')
    list_filter = ('status', 'created_at', 'updated_at', 'wishlist')
    search_fields = ('user__username', 'id')
    readonly_fields = ('created_at', 'updated_at')

# OrderItem Admin
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'price')  # Ensure these fields exist
    list_filter = ('order', 'product')

admin.site.register(OrderItem, OrderItemAdmin)