from .models import Category

def categories_context(request):
    # Fetch categories grouped by their parent category
    product_categories = Category.objects.filter(parent__nav_element="products")
    accessory_categories = Category.objects.filter(parent__nav_element="accessories")
    sale_categories = Category.objects.filter(parent__nav_element="sale")

    return {
        'product_categories': product_categories,
        'accessory_categories': accessory_categories,
        'sale_categories': sale_categories
    }
