from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.core.paginator import Paginator

from .models import Product, Category, ProductFeedback
from wishlist.models import Wishlist, WishlistItem
from .forms import ProductFilterForm, FeedbackForm
from checkout.models import OrderItem


# A view to return all products, sorting, and search
def all_products(request, category_slug=None):
    products = Product.objects.all()
    categories = Category.objects.all()
    query = None
    category = None

    # Initialize the filter form with GET parameters
    form = ProductFilterForm(request.GET)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        subcategories = Category.objects.filter(parent=category)
        products = products.filter(
            category__in=[category] + list(subcategories))

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            # If the search bar is empty, display an error message
            if not query:
                messages.error(request, "No search results found.")
                return redirect(reverse('all_products'))

            product_queries = (
                Q(name__icontains=query)
                | Q(description__icontains=query)
                | Q(subcategory_name__icontains=query)
            )
            category_queries = Q(name__icontains=query)
            products = products.filter(product_queries)
            categories = categories.filter(category_queries)

    form = ProductFilterForm(request.GET)
    products = form.filter_products(products)

    # Paginate the products
    paginator = Paginator(products, 6)  # Show 6 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,
        'categories': categories,
        'category': category,
        'form': form,
        'query': query,
    }

    return render(request, 'products/products.html', context)


# A view to return products by subcategory
def product_by_subcategory(request, subcategory_slug):
    """ Fetch products by subcategory and apply filters. """
    subcategory = get_object_or_404(Category, slug=subcategory_slug)
    products = Product.objects.filter(category=subcategory)

    form = ProductFilterForm(request.GET)
    products = form.filter_products(products)

    return render(
        request, 'products/products.html', {
            'subcategory': subcategory,
            'products': products,
            'form': form,
        }
    )


def product_category(request, category_slug):
    """ Fetch products by category and apply filters. """
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)

    form = ProductFilterForm(request.GET)
    products = form.filter_products(products)

    return render(
        request, 'products/products.html', {
            'category': category,
            'products': products,
            'form': form,
        }
    )


def sale_products(request):
    """ Fetch all products on sale and apply filters. """
    products = Product.objects.filter(discount_price__isnull=False)

    form = ProductFilterForm(request.GET)
    products = form.filter_products(products)

    return render(
        request, 'products/products.html', {
            'products': products,
            'form': form,
        }
    )


def sale_category(request, category_slug):
    """ Fetch sale products by category """
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(
        category=category, discount_price__isnull=False)

    return render(
        request, 'products/products.html', {
            'category': category,
            'products': products,
        }
    )


def all_accessories(request):
    """ Fetch all accessories and apply filters. """
    accessories_category = get_object_or_404(Category, slug='accessories')
    products = Product.objects.filter(category=accessories_category)

    form = ProductFilterForm(request.GET)
    products = form.filter_products(products)

    return render(
        request, 'products/products.html', {
            'category': accessories_category,
            'products': products,
            'form': form,
        }
    )


# A view to return a single product and handle feedback
def product_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user_order_items = OrderItem.objects.filter(
        order__user=request.user, product=product
    ) if request.user.is_authenticated else []

    can_leave_feedback = False
    existing_feedback = None

    if request.user.is_authenticated and user_order_items.exists():
        existing_feedback = ProductFeedback.objects.filter(
            user=request.user, product=product
        ).first()
        if not existing_feedback:
            can_leave_feedback = True

    context = {
        'product': product,
        'form': FeedbackForm(),
        'user_order_items': user_order_items,
        'existing_feedback': existing_feedback,
        'can_leave_feedback': can_leave_feedback,
    }

    return render(request, 'products/product_details.html', context)


@login_required
def create_feedback(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user_order_items = OrderItem.objects.filter(
        order__user=request.user, product=product)

    if not user_order_items.exists():
        messages.error(
            request,
            'You can only leave feedback for products you have ordered.')
        return redirect('product_details', product_id=product.id)

    existing_feedback = ProductFeedback.objects.filter(
        user=request.user, product=product).first()
    if existing_feedback:
        messages.error(
            request, 'You have already submitted feedback for this product.')
        return redirect('product_details', product_id=product.id)

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            order_item_id = request.POST.get('order_item_id')
            order_item = get_object_or_404(
                OrderItem,
                id=order_item_id, order__user=request.user, product=product
            )
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.product = product
            feedback.order_item = order_item
            feedback.save()
            messages.success(request, 'Your feedback has been submitted.')
        else:
            messages.error(
                request, 'There was an error with your feedback submission.')

    return redirect('product_details', product_id=product.id)


@login_required
def update_feedback(request, feedback_id):
    feedback = get_object_or_404(ProductFeedback, id=feedback_id)

    if feedback.user != request.user:
        messages.error(
            request, 'You are not authorized to update this feedback.')
        return redirect('product_details', product_id=feedback.product.id)

    if request.method == 'POST':
        form = FeedbackForm(request.POST, instance=feedback)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your feedback has been updated.')
        else:
            messages.error(
                request, 'There was an error with your feedback update.')

    return redirect('product_details', product_id=feedback.product.id)


@login_required
def delete_feedback(request, feedback_id):
    feedback = get_object_or_404(ProductFeedback, id=feedback_id)

    if feedback.user != request.user:
        messages.error(
            request, 'You are not authorized to delete this feedback.')
        return redirect('product_details', product_id=feedback.product.id)

    feedback.delete()
    messages.success(request, 'Your feedback has been deleted.')
    return redirect('product_details', product_id=feedback.product.id)


@login_required
def add_to_wishlist(request, product_id):
    """Add a product to the user's wishlist."""
    if request.method != "POST":
        return redirect(request.META.get('HTTP_REFERER', 'all_products'))

    product = get_object_or_404(Product, pk=product_id)
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)

    if not WishlistItem.objects.filter(
            wishlist=wishlist, product=product).exists():
        WishlistItem.objects.create(wishlist=wishlist, product=product)

    return redirect(request.META.get('HTTP_REFERER', 'all_products'))


@login_required
def remove_from_wishlist(request, product_id):
    """Remove a product from the user's wishlist."""
    if request.method != "POST":
        return redirect(request.META.get('HTTP_REFERER', 'all_products'))

    product = get_object_or_404(Product, pk=product_id)
    wishlist = get_object_or_404(Wishlist, user=request.user)
    wishlist_item = get_object_or_404(WishlistItem, wishlist=wishlist, product=product)
    wishlist_item.delete()

    return redirect(request.META.get('HTTP_REFERER', 'all_products'))
