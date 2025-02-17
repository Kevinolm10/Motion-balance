from django.contrib import admin
from .models import Product, Category, Tag, ProductImage, ProductFeedback


""" Admin interface for Product model. """


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'subcategory_name',
        'category', 'parent_category',
        'price', 'discount_price',
        'average_rating')
    search_fields = (
        'name',
        'subcategory_name',
        'category__name',
        'parent_category',
        'sizes')
    list_filter = (
        'parent_category',
        'category',
        'tags')
    inlines = [ProductImageInline]


""" Admin interface for Category model. """


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'nav_element')
    search_fields = ('name', 'parent__name')
    list_filter = ('nav_element',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(ProductFeedback)
class ProductFeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'created_at')
    search_fields = ('user__username', 'product__name')
    list_filter = ('rating', 'created_at')
