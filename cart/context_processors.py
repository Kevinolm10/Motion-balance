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
        try:
            product = get_object_or_404(Product, pk=int(item_id))  # Ensure item_id is an integer

            if isinstance(sizes, dict):  # Ensure sizes is a dictionary
                for size, quantity in sizes.items():
                    discounted_price = product.discount_price if product.discount_price else product.price
                    discounted_price = Decimal(str(discounted_price))  # Ensure it's a Decimal
                    subtotal = quantity * discounted_price
                    total += subtotal
                    product_count += quantity

                    # Get product image (fallback to None if no images)
                    image = product.images.first()
                    image_url = image.image.url if image else None
                    alt_text = image.alt_text if image else product.name

                    # Append product details to the cart_items list
                    cart_items.append({
                        'product_id': item_id,
                        'size': size,  # Include size in the cart item
                        'quantity': quantity,
                        'product': product,
                        'subtotal': subtotal,
                        'image_url': image_url,
                        'alt_text': alt_text,
                    })
            else:  # If no sizes, just add the item as a regular product with quantity
                discounted_price = product.discount_price if product.discount_price else product.price
                discounted_price = Decimal(str(discounted_price))  # Ensure it's a Decimal
                subtotal = sizes * discounted_price
                total += subtotal
                product_count += sizes

                image = product.images.first()
                image_url = image.image.url if image else None
                alt_text = image.alt_text if image else product.name

                cart_items.append({
                    'product_id': item_id,
                    'size': None,  # No size for this item
                    'quantity': sizes,
                    'product': product,
                    'subtotal': subtotal,
                    'image_url': image_url,
                    'alt_text': alt_text,
                })

        except Product.DoesNotExist:
            continue  # Skip invalid products instead of breaking the entire cart

    # Fetch settings with default values
    FREE_DELIVERY_THRESHOLD = Decimal(str(getattr(settings, 'FREE_DELIVERY_THRESHOLD', '50.00')))  # Ensure it's a Decimal
    STANDARD_DELIVERY_PERCENTAGE = Decimal(str(getattr(settings, 'STANDARD_DELIVERY_PERCENTAGE', '5.00')))  # Ensure it's a Decimal

    # Calculate delivery costs based on total
    if total < FREE_DELIVERY_THRESHOLD:
        delivery = (total * (STANDARD_DELIVERY_PERCENTAGE / Decimal(100))).quantize(Decimal('0.01'))
        free_delivery_delta = (FREE_DELIVERY_THRESHOLD - total).quantize(Decimal('0.01'))
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
        'free_delivery_threshold': FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context