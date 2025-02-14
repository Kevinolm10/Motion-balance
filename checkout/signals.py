from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Order, OrderItem  # Assuming OrderLineItem was renamed to OrderItem


@receiver(post_save, sender=OrderItem)
@receiver(post_delete, sender=OrderItem)
def update_order_total(sender, instance, **kwargs):
    """
    Update order total whenever an order item is created, updated, or deleted.
    """
    if instance.order:
        instance.order.update_total()


@receiver(post_save, sender=Order)
def handle_order_created_or_updated(sender, instance, created, **kwargs):
    """
    Handle actions when an order is created or updated.
    """
    if created:
        # Perform actions when a new order is created
        print(f"New order created: {instance.order_number}")
        # Example: Send email confirmation, update inventory, etc.
    else:
        # Perform actions when an existing order is updated
        print(f"Order updated: {instance.order_number}")
        # Example: Send notification, update order status, etc.
