from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product


def view_cart(request):
    """ A view to return the cart page """
    cart = request.session.get('cart', {})
    if not cart:
        messages.info(request, 'Your cart is currently empty.')
    return render(request, 'cart/cart.html')


def add_to_cart(request, item_id):
    """ Add a quantity of the specified product to the shopping cart """
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity', 1))
    size = request.POST.get('size')
    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart', {})

    if not isinstance(cart, dict):
        cart = {}

    item_id = str(item_id)

    if item_id not in cart:
        cart[item_id] = {}

    if size in cart[item_id]:
        cart[item_id][size] += quantity
    else:
        cart[item_id][size] = quantity

    request.session['cart'] = cart
    request.session.modified = True

    return redirect(redirect_url)


def delete_from_cart(request, item_id, size):
    """ Remove a specific size of the product from the shopping cart """
    cart = request.session.get('cart', {})

    item_id = str(item_id)

    if item_id in cart:
        if size in cart[item_id]:
            del cart[item_id][size]

            if not cart[item_id]:
                del cart[item_id]

            messages.success(
                request,
                f'Removed size {size} of {item_id} from your cart.'
            )
        else:
            messages.warning(
                request,
                f'Size {size} not found in your cart.'
            )
    else:
        messages.warning(
            request,
            f'Item {item_id} not found in your cart.'
        )

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('view_cart')
