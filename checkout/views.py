from django.shortcuts import render, get_object_or_404
from .models import Order

# Create your views here.

# A view to return all orders
def order_list(request):
    orders = Order.objects.all()
    return render(request, 'checkout/order_list.html', {'orders': orders})

# A view to return a single order
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'checkout/order_detail.html', {'order': order})


def checkout(request):
    """ A view to handle the checkout process """
    return render(request, 'checkout/checkout.html')