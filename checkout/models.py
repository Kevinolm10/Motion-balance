import uuid
from django.db import models
from django.conf import settings
from django.db.models import Sum
from products.models import Product
from wishlist.models import Wishlist

class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    order_number = models.CharField(max_length=32, unique=True, editable=False, default=uuid.uuid4().hex.upper())
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    phone_number = models.CharField(max_length=20)
    shipping_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    postcode = models.CharField(max_length=20, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    wishlist = models.ForeignKey(Wishlist, on_delete=models.SET_NULL, null=True, blank=True)

    def update_total(self):
        self.subtotal = sum(item.total_price for item in self.order_items.all())
        self.delivery_cost = self.calculate_delivery_cost()
        self.grand_total = self.subtotal + self.delivery_cost - self.discount_amount
        self.save()

    def calculate_delivery_cost(self):
        FREE_SHIPPING_THRESHOLD = 50  # Example threshold
        STANDARD_DELIVERY_PERCENTAGE = 5  # Example percentage
        
        if self.subtotal < FREE_SHIPPING_THRESHOLD:
            return self.subtotal * (STANDARD_DELIVERY_PERCENTAGE / 100)
        return 0

    def __str__(self):
        return f"Order {self.order_number} - {self.status}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)  # Store product name in case it changes
    product_price = models.DecimalField(max_digits=10, decimal_places=2)  # Store price at purchase time
    quantity = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    
    size = models.CharField(max_length=10, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.total_price = self.product_price * self.quantity  # Calculate line item total
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.product_name} (x{self.quantity}) - Order {self.order.order_number}'
