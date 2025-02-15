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
    sizes = []  # Default sizes should be empty or None

    if product_id:
        product = get_object_or_404(Product, pk=product_id)

        # If the product is not an accessory, split the sizes string
        if product.parent_category != 'accessories':
            sizes = product.sizes.split(',') if product.sizes else []  # Convert sizes string to list
        else:
            # For accessories, ensure sizes is empty or None
            sizes = []

    return {
        "product": product,
        "sizes": sizes,  # Pass the sizes as a list (empty if accessory)
    }
