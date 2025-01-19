from django.shortcuts import render
from .models import Product

# Create your views here.
def all_products(request):
    """ A view to return the products, sorting and search """

    product = Product.objects.all()

    context = {
        'products' : products,
    }

    return render(request, 'products/products.html', context)



def product_category(request, category_slug):
    try:
        category = Category.objects.get(slug=category_slug)
        products = Product.objects.filter(category=category)  # Adjust filtering as necessary
    except Category.DoesNotExist:
        products = []  # Or handle the error accordingly

    return render(request, 'products/product_category.html', {
        'category': category,
        'products': products,
    })