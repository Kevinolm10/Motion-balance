from .models import Category
from products.models import Product
from django.shortcuts import get_object_or_404


""" Context processors for the products app. """


def categories_context(request):
    product_categories = Category.objects.filter(
        parent__nav_element="products")
    accessory_categories = Category.objects.filter(
        parent__nav_element="accessories")
    sale_categories = Category.objects.filter(parent__nav_element="sale")

    return {
        'product_categories': product_categories,
        'accessory_categories': accessory_categories,
        'sale_categories': sale_categories
    }


def product_details_context(request):
    """Context processor to provide product details globally where needed."""
    product_id = request.GET.get("product_id")
    product = None
    sizes = []

    if product_id:
        product = get_object_or_404(Product, pk=product_id)

        if product.parent_category != 'accessories':
            sizes = product.sizes.split(',') if product.sizes else []
        else:
            sizes = []

    return {
        "product": product,
        "sizes": sizes,
    }
