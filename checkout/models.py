import uuid
from decimal import Decimal
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
    order_number = models.CharField(max_length=32, unique=True, editable=False)
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

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = uuid.uuid4().hex.upper()  # Generate a unique order number
        super().save(*args, **kwargs)

    def update_total(self):
        # Update subtotal, delivery cost, and grand total
        self.subtotal = self.order_items.aggregate(Sum('total_price'))['total_price__sum'] or Decimal('0.00')
        self.delivery_cost = self.calculate_delivery_cost()
        self.discount_amount = Decimal(str(self.discount_amount))  # Ensure discount_amount is a Decimal
        self.grand_total = (self.subtotal + self.delivery_cost - self.discount_amount).quantize(Decimal('0.01'))
        self.save()

    def calculate_delivery_cost(self):
        FREE_SHIPPING_THRESHOLD = Decimal('50.00')  # Example threshold for free shipping
        STANDARD_DELIVERY_PERCENTAGE = Decimal('5.00')  # Delivery cost percentage for standard delivery
        
        if self.subtotal < FREE_SHIPPING_THRESHOLD:
            return (self.subtotal * (STANDARD_DELIVERY_PERCENTAGE / Decimal('100.00'))).quantize(Decimal('0.01'))
        return Decimal('0.00')  # Free shipping if subtotal exceeds the threshold

    def __str__(self):
        return f"Order {self.order_number} - {self.status}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)  # Store product name at purchase time
    product_price = models.DecimalField(max_digits=10, decimal_places=2)  # Store price at purchase time
    quantity = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    
    size = models.CharField(max_length=10, null=True, blank=True)  # Optional size field (if applicable)

    def save(self, *args, **kwargs):
        self.total_price = self.product_price * self.quantity  # Calculate total price for this line item
        super().save(*args, **kwargs)
        self.order.update_total()  # Ensure that the total order price gets updated when this item is saved

    def __str__(self):
        return f'{self.product_name} (x{self.quantity}) - Order {self.order.order_number}'