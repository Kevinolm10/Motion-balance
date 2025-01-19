from .models import Category

def categories_context(request):
    return {
        'product_categories': Category.objects.filter(nav_element='products'),
        'accessory_categories': Category.objects.filter(nav_element='accessories'),
        'sale_categories': Category.objects.filter(nav_element='sale'),
    }