from decimal import Decimal
from django.db import models
from django.db.models import Sum
from products.models import Product


class Order(models.Model):
    """
    Model representing an order.
    """
    order_number = models.CharField(max_length=32, null=False, editable=False)
    user = models.ForeignKey(
        'auth.User', on_delete=models.SET_NULL, null=True, blank=True
    )
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = models.CharField(max_length=40, null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    city = models.CharField(max_length=40, null=False, blank=False)
    shipping_address = models.CharField(max_length=80, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    subtotal = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0
    )
    delivery_cost = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0
    )
    discount_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0
    )
    grand_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0
    )
    status = models.CharField(max_length=20, null=False, blank=False)

    def update_total(self):
        """
        Update subtotal, delivery cost, and grand total.
        """
        self.subtotal = (
            self.order_items.aggregate(Sum('total_price'))['total_price__sum']
            or Decimal('0.00')
        )
        self.delivery_cost = self.calculate_delivery_cost()
        self.discount_amount = Decimal(str(self.discount_amount))
        self.grand_total = (
            self.subtotal + self.delivery_cost - self.discount_amount
        ).quantize(Decimal('0.01'))
        self.save()

    def calculate_delivery_cost(self):
        """
        Calculate the delivery cost based on the subtotal.
        """
        FREE_SHIPPING_THRESHOLD = Decimal('50.00')
        STANDARD_DELIVERY_PERCENTAGE = Decimal('5.00')

        if self.subtotal < FREE_SHIPPING_THRESHOLD:
            return (self.subtotal * (
                STANDARD_DELIVERY_PERCENTAGE / Decimal('100.00')
            )).quantize(Decimal('0.01'))
        return Decimal('0.00')

    def __str__(self):
        return f"Order {self.order_number} - {self.status}"


class OrderItem(models.Model):
    """
    Model representing an item within an order.
    """
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='order_items'
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=1)
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, editable=False
    )
    size = models.CharField(max_length=10, null=True, blank=True)

    def save(self, *args, **kwargs):
        """
        Override the save method to set the total price and update order total.
        """
        self.total_price = self.product_price * self.quantity
        super().save(*args, **kwargs)
        self.order.update_total()

    def __str__(self):
        return (
            f"{self.product_name} (x{self.quantity}) - "
            f"Order {self.order.order_number}"
        )
