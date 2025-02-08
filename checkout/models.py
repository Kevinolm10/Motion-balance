from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from wishlist.models import Wishlist  # Import the Wishlist model

# Order Model
class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # New field to track if the order originated from a wishlist
    wishlist = models.ForeignKey(Wishlist, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Order {self.id} - {self.status}"

    def calculate_total_price(self):
        self.total_price = sum(item.total_price for item in self.order_items.all())
        self.save()


# Order Item Model
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} pcs"
