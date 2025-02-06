from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Category

@receiver(post_migrate)
def create_parent_categories(sender, **kwargs):
    Category.create_parent_categories()