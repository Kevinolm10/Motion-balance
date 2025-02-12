from .models import Category
from products.models import Product
from django.shortcuts import get_object_or_404

def categories_context(request):
    # Fetch categories grouped by their parent category
    product_categories = Category.objects.filter(parent__nav_element="products")
    accessory_categories = Category.objects.filter(parent__nav_element="accessories")
    sale_categories = Category.objects.filter(parent__nav_element="sale")

     # Return the categories as a dictionary
    return {
        'product_categories': product_categories,
        'accessory_categories': accessory_categories,
        'sale_categories': sale_categories
    }


def product_details_context(request):
    """Context processor to provide product details globally where needed."""
    product_id = request.GET.get("product_id")  # Get product ID from URL query parameters
    product = None
    sizes = ['S', 'M', 'L', 'XL']  # Default sizes

    if product_id:
        product = get_object_or_404(Product, pk=product_id)
        sizes = product.sizes.split(',') if product.sizes else []  # Convert sizes string to list

    return {
        "product": product,
        "sizes": sizes,  # Pass the sizes as a list
    }

