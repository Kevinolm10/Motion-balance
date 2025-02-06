from django.db import models
from products.models import Product
from django.contrib.auth.models import User

# Create your models here.

# Wishlist Model
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')  # Prevent duplicate wishlisted items

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
