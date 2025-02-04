from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category  # <-- Import Category here

# Create your views here.
def all_products(request):
    """ A view to return the products, sorting, and search """
    products = Product.objects.all()

    query = None

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "No search results found.")
                return redirect(reverse('products'))
            
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    context = {
        'products': products,
        'search_term': query,
    }

    return render(request, 'products/products.html', context)


def product_by_subcategory(request, subcategory_slug):
    # Get the subcategory based on the slug
    subcategory = get_object_or_404(Category, slug=subcategory_slug)

    # Filter products by subcategory
    products = Product.objects.filter(category=subcategory)

    # Render the products page with the filtered products
    return render(request, 'products/products.html', {
        'subcategory': subcategory,
        'products': products
    })



def product_category(request, category_slug):
    # Get the category based on the slug
    category = get_object_or_404(Category, slug=category_slug)

    # Filter products by category
    products = Product.objects.filter(category=category)

    # Render the same template but with the filtered products
    return render(request, 'products/products.html', {
        'category': category,
        'products': products
    })

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
