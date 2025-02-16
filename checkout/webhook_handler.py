import logging
from django.http import HttpResponse
from .models import Order, OrderItem
from products.models import Product
import json
import time
import stripe  # Ensure this import is at the top of the file

# Configure logging
logger = logging.getLogger(__name__)

class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        logger.info(f'Unhandled webhook received: {event["type"]}')
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200
        )

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        intent = event.data.object
        pid = intent.id
        metadata = intent.metadata if hasattr(intent, 'metadata') else None
        cart = metadata.get('cart', None) if metadata else None
        save_info = metadata.get('save_info', None) if metadata else None

        if not cart:
            logger.error(f'Missing cart data for PaymentIntent: {pid}')
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | ERROR: Missing cart data for PaymentIntent: {pid}',
                status=500
            )

        # Check if charges attribute exists
        if hasattr(intent, 'charges') and intent.charges.data:
            billing_details = intent.charges.data[0].billing_details
            shipping_details = intent.shipping
            grand_total = round(intent.charges.data[0].amount / 100, 2)
        else:
            logger.error(f'Missing charges data for PaymentIntent: {pid}')
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | ERROR: Missing charges data for PaymentIntent: {pid}',
                status=500
            )

        # Clean data in the shipping details
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    full_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=shipping_details.phone,
                    country__iexact=shipping_details.address.country,
                    postcode__iexact=shipping_details.address.postal_code,
                    city__iexact=shipping_details.address.city,
                    shipping_address__iexact=shipping_details.address.line1,
                    grand_total=grand_total,
                    original_cart=cart,
                    stripe_pid=pid,
                )
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)
        if order_exists:
            logger.info('Verified order already in database')
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: '
                        f'Verified order already in database',
                status=200
            )
        else:
            order = None
            try:
                order = Order.objects.create(
                    full_name=shipping_details.name,
                    email=billing_details.email,
                    phone_number=shipping_details.phone,
                    country=shipping_details.address.country,
                    postcode=shipping_details.address.postal_code,
                    city=shipping_details.address.city,
                    shipping_address=shipping_details.address.line1,
                    original_cart=cart,
                    stripe_pid=pid,
                    grand_total=grand_total,
                )
                for item_id, item_data in json.loads(cart).items():
                    product = Product.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        order_item = OrderItem(
                            order=order,
                            product=product,
                            product_name=product.name,
                            product_price=product.price,
                            quantity=item_data,
                        )
                        order_item.save()
                    else:
                        for size, quantity in item_data['items_by_size'].items():
                            order_item = OrderItem(
                                order=order,
                                product=product,
                                product_name=product.name,
                                product_price=product.price,
                                quantity=quantity,
                                size=size,
                            )
                            order_item.save()
            except Exception as e:
                if order:
                    order.delete()
                logger.error(f'Error creating order: {e}')
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500
                )
            logger.info('Created order in webhook')
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: '
                f'Created order in webhook',
                status=200
            )

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        logger.info(f'Webhook received: {event["type"]}')
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
        )