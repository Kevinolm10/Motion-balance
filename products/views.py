from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required  # Import login_required
from django.db.models import Q
from .models import Product, Category
from wishlist.models import Wishlist, WishlistItem
from .forms import ProductFilterForm
from .forms import FeedbackForm
from checkout.models import OrderItem
from django.http import JsonResponse  

# A view to return all products, sorting, and search
def all_products(request, category_slug=None):
    products = Product.objects.all()
    categories = Category.objects.all()
    query = None
    category = None

    # Initialize the filter form with GET parameters
    form = ProductFilterForm(request.GET)

    # If a category slug is provided, filter products by category and its subcategories
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        subcategories = Category.objects.filter(parent=category)
        products = products.filter(category__in=[category] + list(subcategories))

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

    form = ProductFilterForm(request.GET)
    products = form.filter_products(products)


    context = {
        'products': products,
        'categories': categories,
        'category': category,
        'form': form,
        'query': query,
    }

    return render(request, 'products/products.html', context)


# A view to return a single product
def product_by_subcategory(request, subcategory_slug):
    """ Fetch products by subcategory and apply filters. """
    subcategory = get_object_or_404(Category, slug=subcategory_slug)
    products = Product.objects.filter(category=subcategory)

    form = ProductFilterForm(request.GET)
    products = form.filter_products(products)  # Apply filters using the form method

    return render(request, 'products/products.html', {
        'subcategory': subcategory,
        'products': products,
        'form': form,
    })



def product_category(request, category_slug):
    """ Fetch products by category and apply filters. """
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)

    form = ProductFilterForm(request.GET)
    products = form.filter_products(products)  # Apply filters using the form method

    return render(request, 'products/products.html', {
        'category': category,
        'products': products,
        'form': form
    })




def sale_products(request):
    """ Fetch all products on sale and apply filters. """
    products = Product.objects.filter(discount_price__isnull=False)
    
    form = ProductFilterForm(request.GET)
    products = form.filter_products(products)  # Apply filters using the form method

    return render(request, 'products/products.html', {'products': products, 'form': form})


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
    accessories_category = get_object_or_404(Category, slug='accessories')
    products = Product.objects.filter(category=accessories_category)

    form = ProductFilterForm(request.GET)
    products = form.filter_products(products)

    return render(request, 'products/products.html', {
        'category': accessories_category,
        'products': products,
        'form': form
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
    """Add a product to the user's wishlist."""
    if request.method != "POST":
        return redirect(request.META.get('HTTP_REFERER'))  # Go back to the referring page

    product = get_object_or_404(Product, pk=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)

    if WishlistItem.objects.filter(wishlist=wishlist, product=product).exists():
        return redirect(request.META.get('HTTP_REFERER'))  # Go back to the referring page
    
    WishlistItem.objects.create(wishlist=wishlist, product=product)
    
    return redirect(request.META.get('HTTP_REFERER'))  # Go back to the referring page

@login_required
def remove_from_wishlist(request, product_id):
    """Remove a product from the user's wishlist."""
    if request.method != "POST":
        return redirect(request.META.get('HTTP_REFERER'))  # Go back to the referring page

    product = get_object_or_404(Product, pk=product_id)
    wishlist = get_object_or_404(Wishlist, user=request.user)
    wishlist_item = get_object_or_404(WishlistItem, wishlist=wishlist, product=product)
    wishlist_item.delete()

    return redirect(request.META.get('HTTP_REFERER'))  # Go back to the referring page