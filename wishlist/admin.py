from django.contrib import admin
from .models import Wishlist, WishlistItem


"""Admin interface for Wishlist and WishlistItem models."""


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)


@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ('wishlist', 'product', 'created_at')
    list_filter = ('created_at', 'wishlist', 'product')
    search_fields = ('wishlist__user__username', 'product__name')
