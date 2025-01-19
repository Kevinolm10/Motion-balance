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
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(request, 'products/category_products.html', {'category': category, 'products': products})

def sale_products(request):
    products = Product.objects.filter(discount_price__isnull=False)
    return render(request, 'products/sale_products.html', {'products': products})

def sale_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category, discount_price__isnull=False)
    return render(request, 'products/sale_category_products.html', {'category': category, 'products': products})

def all_accessories(request):
    # Fetch all products in the "accessories" category
    accessories = Product.objects.filter(category__slug='accessories')
    return render(request, 'products/accessories.html', {'accessories': accessories})