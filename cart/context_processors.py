from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product

def cart_items(request):
    cart_items = []
    total = Decimal('0.00')
    product_count = 0
    cart = request.session.get('cart', {})

    # Ensure cart is a dictionary
    if not isinstance(cart, dict):
        cart = {}

    for item_id, sizes in cart.items():
        product = get_object_or_404(Product, pk=int(item_id))  # Get product details by ID

        # sizes is expected to be a dictionary: size -> quantity
        if isinstance(sizes, dict):  
            for size, quantity in sizes.items():  # Loop through sizes and quantities
                discounted_price = product.discount_price if product.discount_price else product.price
                subtotal = quantity * discounted_price
                total += subtotal
                product_count += quantity
                image_url = product.images.first().image.url if product.images.exists() else None
                alt_text = product.images.first().alt_text if product.images.exists() else product.name

                # Append the product details to the cart_items list
                cart_items.append({
                    'product_id': item_id,
                    'size': size,  # Include size in the cart item
                    'quantity': quantity,
                    'product': product,
                    'subtotal': subtotal,
                    'image_url': image_url,
                    'alt_text': alt_text,
                })

    # Calculate delivery costs based on total
    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = (total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE) / Decimal(100)).quantize(Decimal('0.01'))
        free_delivery_delta = (settings.FREE_DELIVERY_THRESHOLD - total).quantize(Decimal('0.01'))
    else:
        delivery = Decimal('0.00')
        free_delivery_delta = Decimal('0.00')

    # Calculate grand total
    grand_total = (delivery + total).quantize(Decimal('0.01'))  # Ensure proper rounding to 2 decimal places

    # Context to pass to the template
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
