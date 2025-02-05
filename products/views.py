from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category

# A view to return all products, sorting, and search
def all_products(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    query = None

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            # If the search bar is empty, display an error message
            if not query:
                messages.error(request, "No search results found.")
                return redirect(reverse('all_products'))
            
            product_queries = Q(name__icontains=query) | Q(description__icontains=query) | Q(subcategory_name__icontains=query)
            category_queries = Q(name__icontains=query)
            products = products.filter(product_queries)
            categories = categories.filter(category_queries)

    context = {
        'products': products,
        'categories': categories,
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
    # Fetch all products on sale (discount price is not null)
    products = Product.objects.filter(discount_price__isnull=False)

    # Render the same template with the filtered products
    return render(request, 'products/products.html', {'products': products})


def sale_category(request, category_slug):
    # Fetch the category based on the slug
    category = get_object_or_404(Category, slug=category_slug)
    
    # Fetch all products in the category that are on sale (discount price is not null)
    products = Product.objects.filter(category=category, discount_price__isnull=False)

    # Render the products page with the filtered products
    return render(request, 'products/products.html', {
        'category': category,
        'products': products
    })


def all_accessories(request):
    # Fetch the accessories category
    accessories_category = get_object_or_404(Category, slug='accessories')

    # Fetch all products in the accessories category
    products = Product.objects.filter(category=accessories_category)

    # Render the same products page with the filtered products
    return render(request, 'products/products.html', {
        'category': accessories_category,
        'products': products
    })
