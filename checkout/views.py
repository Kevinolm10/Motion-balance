import json
import stripe
from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.contrib import messages
from django.conf import settings
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from .forms import OrderForm
from .models import Order, OrderItem
from products.models import Product
from cart.context_processors import cart_items


@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        
        # Get cart data from session
        cart_data = request.session.get('cart', {})
        if not cart_data:
            raise ValueError("No cart data found")

        # Modify the PaymentIntent with cart data
        stripe.PaymentIntent.modify(pid, metadata={
            'cart_items': json.dumps(cart_data),  # Store cart items in metadata
            'save_info': request.POST.get('save_info'),
            'username': request.user.username,  # Ensure username is correctly stored
        })

        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be processed right now. Please try again later.')
        return HttpResponse(content=str(e), status=400)


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "There's nothing in your cart at the moment")
        return redirect(reverse('all_products'))

    current_cart = cart_items(request)
    total = current_cart['grand_total']
    stripe_total = round(total * 100)
    stripe.api_key = stripe_secret_key

    try:
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )
    except stripe.error.StripeError:
        messages.error(
            request,
            "There was an issue with payment. Please try again.")
        return redirect(reverse('checkout'))

    if request.method == 'POST':
        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'shipping_address': request.POST['shipping_address'],
            'city': request.POST['city'],
            'postcode': request.POST['postcode'],
            'country': request.POST['country'],
        }

        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)

            # Check if the user is authenticated
            if request.user.is_authenticated:
                order.user = request.user
            else:
                # If not authenticated, create or get a guest user
                guest_user, created = User.objects.get_or_create(
                    username='guest',
                    email=request.POST['email'])
                order.user = guest_user  # Assign guest user

            order.stripe_pid = intent.id
            order.original_cart = cart
            order.total_price = total
            order.save()

            # Create order items from the cart
            for item_id, item_data in cart.items():
                try:
                    product = Product.objects.get(id=item_id)
                    if isinstance(item_data, int):  # Product without size
                        order_item = OrderItem(
                            order=order,
                            product=product,
                            product_name=product.name,
                            product_price=product.price,
                            quantity=item_data,
                        )
                        order_item.save()
                    else:  # Product with sizes
                        for size, quantity in item_data.items():
                            order_item = OrderItem(
                                order=order,
                                product=product,
                                product_name=product.name,
                                product_price=product.price,
                                quantity=quantity,
                                size=size,
                            )
                            order_item.save()
                except Product.DoesNotExist:
                    messages.error(request, (
                        "One of the products in your cart wasn't found. "
                        "Please email us for assistance!"
                    ))
                    order.delete()
                    return redirect(reverse('view_cart'))

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse(
                'checkout_success', args=[order.order_number]))
        else:
            messages.error(request,
            'There was an error with your form. Check your information.')
    else:
        order_form = OrderForm()

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)


def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)
    messages.success(
        request, f'Order successfully processed! Your order number is {order_number}. A confirmation email will be sent to {order.email}.')

    if 'cart' in request.session:
        del request.session['cart']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)


def order_detail(request, order_id):
    # Fetch the order using the provided order ID
    order = get_object_or_404(Order, id=order_id)

    # Pass the order to the template
    return render(request, 'order_detail.html', {'order': order})
