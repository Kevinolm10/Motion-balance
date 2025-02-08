from django.contrib import admin
from .models import Product, Category, Tag, ProductVariant, ProductImage, ProductFeedback

# Register your models here.
# Product Admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'subcategory_name', 'category', 'parent_category', 'price', 'discount_price', 'average_rating')
    search_fields = ('name', 'subcategory_name', 'category__name', 'parent_category')
    list_filter = ('parent_category', 'category', 'tags')

# Category Admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'nav_element', 'created_at', 'updated_at')
    search_fields = ('name', 'parent__name')
    list_filter = ('nav_element', 'created_at', 'updated_at')

# Tag Admin
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Product Variant Admin
@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'size', 'color', 'price')
    search_fields = ('product__name', 'size', 'color')
    list_filter = ('size', 'color')

# Product Image Admin
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image', 'alt_text')
    search_fields = ('product__name', 'alt_text')

# Product Feedback Admin
@admin.register(ProductFeedback)
class ProductFeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'created_at')
    search_fields = ('user__username', 'product__name')
    list_filter = ('rating', 'created_at')