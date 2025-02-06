# Django Imports
from django.contrib import admin
# Local Imports
from .models import Category, Product, ProductFeedback

# Category Admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'nav_element', 'parent', 'created_at', 'updated_at')
    list_filter = ('nav_element', 'parent')
    search_fields = ('name', 'slug')
    list_display_links = ('name',)  # Makes the category name clickable
    ordering = ('name',)  # Orders categories alphabetically by name
    
    # Use a custom method to display parent category name in a better way
    def parent(self, obj):
        return obj.parent.name if obj.parent else "None"
    parent.short_description = 'Parent Category'

# Product Admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'discount_percentage', 'discount_price', 'average_rating', 'subcategory_name', 'category_name')
    list_filter = ('category', 'parent_category')
    search_fields = ('name', 'description')
    readonly_fields = ('discount_price',)

    def average_rating(self, obj):
        return obj.average_rating()
    average_rating.short_description = 'Average Rating'

    def subcategory_name(self, obj):
        return obj.category.name if obj.category else 'No subcategory'
    subcategory_name.short_description = 'Subcategory'

    # Custom method to display the category name in list view
    def category_name(self, obj):
        return obj.category.name if obj.category else 'No category'
    category_name.short_description = 'Category'


# ProductFeedback Admin
@admin.register(ProductFeedback)
class ProductFeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'product__name', 'comment')
    readonly_fields = ('created_at',)

