from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order

# Create a signal to handle order creation and updates
@receiver(post_save, sender=Order)
def order_created_or_updated(sender, instance, created, **kwargs):
    if created:
        # Perform actions when a new order is created
        print(f"New order created: {instance}")
        # You can add code here to send notifications, update inventory, etc.
    else:
        # Perform actions when an existing order is updated
        print(f"Order updated: {instance}")
        # You can add code here to send notifications, update order status, etc.