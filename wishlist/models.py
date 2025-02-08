from django.db import models
from products.models import Product
from django.contrib.auth.models import User

# Wishlist Model (One per user)
class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wishlist')

    def __str__(self):
        return f"{self.user.username}'s Wishlist"

# Wishlist Items (Multiple per Wishlist)
class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('wishlist', 'product')  # Prevent duplicates

    def __str__(self):
        return f"{self.wishlist.user.username} - {self.product.name}"
