from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product

def cart_items(request):
    cart_items = []
    total = Decimal('0.00')
    product_count = 0
    cart = request.session.get('cart', {})

    for item_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=item_id)
        subtotal = quantity * product.discount_price  # Use the discounted price from the model
        total += subtotal
        product_count += quantity
        image_url = product.images.first().image.url if product.images.exists() else None
        alt_text = product.images.first().alt_text if product.images.exists() else ''
        cart_items.append({
            'product_id': item_id,
            'quantity': quantity,
            'product': product,
            'subtotal': subtotal,
            'image_url': image_url,
            'alt_text': alt_text,
        })

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = Decimal('0.00')
        free_delivery_delta = Decimal('0.00')

    grand_total = delivery + total

    context = {
        'cart_items': cart_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context