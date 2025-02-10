from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required  # Import login_required
from django.db.models import Q
from .models import Product, Category
from wishlist.models import Wishlist, WishlistItem
from .forms import ProductFilterForm
from .forms import FeedbackForm
from checkout.models import OrderItem

# A view to return all products, sorting, and search
def all_products(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    query = None

    # Initialize the filter form with GET parameters
    form = ProductFilterForm(request.GET)

    # If the search bar is used, filter products by name, description, or subcategory
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

        # Apply filters from the form
        if form.is_valid():
            if form.cleaned_data['min_price']:
                products = products.filter(price__gte=form.cleaned_data['min_price'])
            if form.cleaned_data['max_price']:
                products = products.filter(price__lte=form.cleaned_data['max_price'])
            if form.cleaned_data['min_discount']:
                products = products.filter(discount_percentage__gte=form.cleaned_data['min_discount'])
            if form.cleaned_data['max_discount']:
                products = products.filter(discount_percentage__lte=form.cleaned_data['max_discount'])
            if form.cleaned_data['min_rating']:
                products = products.filter(average_rating__gte=form.cleaned_data['min_rating'])
            if form.cleaned_data['max_rating']:
                products = products.filter(average_rating__lte=form.cleaned_data['max_rating'])

    context = {
        'products': products,
        'categories': categories,
        'search_term': query,
        'form': form,
    }

    return render(request, 'products/products.html', context)


# A view to return a single product
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

@login_required
def product_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user_order_items = OrderItem.objects.filter(order__user=request.user, product=product)

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            order_item_id = request.POST.get('order_item_id')
            order_item = get_object_or_404(OrderItem, id=order_item_id, order__user=request.user, product=product)
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.product = product
            feedback.order_item = order_item
            feedback.save()
            messages.success(request, 'Your feedback has been submitted.')
            return redirect('product_details', product_id=product.id)
    else:
        form = FeedbackForm()

    context = {
        'product': product,
        'form': form,
        'user_order_items': user_order_items,
    }
    return render(request, 'products/product_details.html', context)

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist_item, created = WishlistItem.objects.get_or_create(wishlist=wishlist, product=product)
    if created:
        messages.success(request, f"{product.name} has been added to your wishlist.")
    else:
        messages.info(request, f"{product.name} is already in your wishlist.")
    return redirect('product_detail', product_id=product.id)

@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist = get_object_or_404(Wishlist, user=request.user)
    wishlist_item = get_object_or_404(WishlistItem, wishlist=wishlist, product=product)
    wishlist_item.delete()
    messages.success(request, f"{product.name} has been removed from your wishlist.")
    return redirect('product_detail', product_id=product.id)
