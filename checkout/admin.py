from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('product', 'quantity', 'price')
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'status', 'created_at', 'grand_total')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('order_number', 'user__username', 'full_name', 'email')
    readonly_fields = ('order_number', 'created_at', 'updated_at', 'grand_total', 'transaction_id', 'payment_method')
    fieldsets = (
        (None, {
            'fields': ('order_number', 'user', 'status', 'created_at', 'updated_at')
        }),
        ('Contact Information', {
            'fields': ('full_name', 'email', 'phone_number')
        }),
        ('Shipping Information', {
            'fields': ('shipping_address', 'billing_address', 'city', 'country', 'postcode')
        }),
        ('Order Details', {
            'fields': ('subtotal', 'delivery_cost', 'discount_amount', 'grand_total', 'transaction_id', 'payment_method', 'wishlist')
        }),
    )
    inlines = [OrderItemInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')
    search_fields = ('order__order_number', 'product__name')
    readonly_fields = ('order', 'product', 'quantity', 'price')