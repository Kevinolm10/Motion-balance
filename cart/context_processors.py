from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product
import stripe
import logging

# Set up logging
logger = logging.getLogger(__name__)

def cart_items(request):
    """
    Retrieve and process cart items from the session, calculate totals,
    and return cart details.
    """
    cart_items = []
    total = Decimal('0.00')
    product_count = 0
    cart = request.session.get('cart', {})

    if not isinstance(cart, dict):
        cart = {}

    for item_id, sizes in cart.items():
        try:
            product = get_object_or_404(Product, pk=int(item_id))

            if isinstance(sizes, dict):
                for size, quantity in sizes.items():
                    discounted_price = (
                        product.discount_price
                        if product.discount_price
                        else product.price
                    )
                    discounted_price = Decimal(str(discounted_price))
                    subtotal = quantity * discounted_price
                    total += subtotal
                    product_count += quantity

                    image = product.images.first()
                    image_url = image.image.url if image else None
                    alt_text = image.alt_text if image else product.name

                    cart_items.append({
                        'product_id': item_id,
                        'size': size,
                        'quantity': quantity,
                        'product': product,
                        'subtotal': subtotal,
                        'image_url': image_url,
                        'alt_text': alt_text,
                    })
            else:
                discounted_price = (
                    product.discount_price
                    if product.discount_price
                    else product.price
                )
                discounted_price = Decimal(str(discounted_price))
                subtotal = sizes * discounted_price
                total += subtotal
                product_count += sizes

                image = product.images.first()
                image_url = image.image.url if image else None
                alt_text = image.alt_text if image else product.name

                cart_items.append({
                    'product_id': item_id,
                    'size': None,
                    'quantity': sizes,
                    'product': product,
                    'subtotal': subtotal,
                    'image_url': image_url,
                    'alt_text': alt_text,
                })

        except Product.DoesNotExist:
            # Log missing product IDs for debugging
            logger.error(f"Product with ID {item_id} does not exist in the database.")
            continue  # Continue with the next item in the cart

    FREE_DELIVERY_THRESHOLD = Decimal(
        str(getattr(settings, 'FREE_DELIVERY_THRESHOLD', '50.00'))
    )
    STANDARD_DELIVERY_PERCENTAGE = Decimal(
        str(getattr(settings, 'STANDARD_DELIVERY_PERCENTAGE', '5.00'))
    )

    if total < FREE_DELIVERY_THRESHOLD:
        delivery = (
            total * (STANDARD_DELIVERY_PERCENTAGE / Decimal(100))
        ).quantize(Decimal('0.01'))
        free_delivery_delta = (
            FREE_DELIVERY_THRESHOLD - total
        ).quantize(Decimal('0.01'))
    else:
        delivery = Decimal('0.00')
        free_delivery_delta = Decimal('0.00')

    grand_total = (delivery + total).quantize(Decimal('0.01'))

    line_items = []
    for cart_item in cart_items:
        product = cart_item['product']
        line_items.append({
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': product.name,
                },
                'unit_amount': int(cart_item['subtotal'] * 100),
            },
            'quantity': cart_item['quantity'],
        })

    metadata = {
        'cart_items': ', '.join([
            f'{item["product"].name} (x{item["quantity"]})'
            for item in cart_items
        ])
    }

    context = {
        'cart_items': cart_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
        'line_items': line_items,
        'metadata': metadata,
    }

    return context
