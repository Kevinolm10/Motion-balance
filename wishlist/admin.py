from django.contrib import admin
from .models import Wishlist, WishlistItem


# Register your models here.
# Wishlist Admin
@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)


# WishlistItem Admin
@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ('wishlist', 'product', 'created_at')
    list_filter = ('created_at', 'wishlist', 'product')
    search_fields = ('wishlist__user__username', 'product__name')