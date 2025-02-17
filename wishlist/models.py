from django.db import models
from products.models import Product
from django.contrib.auth.models import User


"""Model for user wishlist."""


class Wishlist(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='wishlist')

    def __str__(self):
        return f"{self.user.username}'s Wishlist"


"""Model for wishlist item."""


class WishlistItem(models.Model):
    wishlist = models.ForeignKey(
        Wishlist,
        on_delete=models.CASCADE,
        related_name='items')
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('wishlist', 'product')

    def __str__(self):
        return f"{self.wishlist.user.username} - {self.product.name}"
