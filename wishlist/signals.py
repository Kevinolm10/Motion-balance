from django.db.models.signals import post_save
from django.dispatch import receiver
from user_profile.models import UserProfile  # Updated import path
from .models import Wishlist

@receiver(post_save, sender=UserProfile)
def create_wishlist(sender, instance, created, **kwargs):
    """Automatically create an empty wishlist for new users."""
    if created:
        Wishlist.objects.create(user=instance.user)
