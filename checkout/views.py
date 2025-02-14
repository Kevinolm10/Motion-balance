from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import OrderForm

# Create your views here.

# A view to return all orders
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('products'))
    
    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51QsRU8C8aDPhUZEVLrD8C5h8Pvgmn87NImXMbktJtbr94RQfCMkDdIQfUAAxLLgE6lUr4g08cS3uKDvy1vq2QV4u00pdpCBz91',
        'client_secret': 'test client secret',
    }

    return render(request, template, context)

