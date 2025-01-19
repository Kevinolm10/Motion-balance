from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']  # Categories are ordered alphabetically by name

    def __str__(self):
        return self.name


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.FloatField(null=True, blank=True)  # Discount percentage (e.g., 20)
    discount_price = models.FloatField(null=True, blank=True)  # Final price after discount
    product_image = models.ImageField(upload_to='products/')

    def save(self, *args, **kwargs):
        """Override save method to calculate discount price when saving the product."""
        if self.discount_percentage:
            self.discount_price = self.price * (1 - self.discount_percentage / 100)
        super().save(*args, **kwargs)

    def average_rating(self):
        from django.db.models import Avg
        avg_rating = self.productfeedback_set.aggregate(Avg('rating'))['rating__avg']
        return round(avg_rating, 2) if avg_rating else None

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
    ]

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.id} - {self.status}"

    def calculate_total_price(self):
        self.total_price = sum(item.total_price for item in self.order_items.all())
        self.save()


class OrderItem(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"OrderItem {self.id} - {self.product.name}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class ProductFeedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE)

    def __str__(self):
        return f"Feedback {self.feedback_id} - {self.product.name}"


class Wishlist(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Wishlist {self.id} - {self.product.name}"