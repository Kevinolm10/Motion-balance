from django.urls import path
from .views import view_cart, add_to_cart, delete_from_cart


# URL patterns for the cart app
urlpatterns = [
    path(
        '',
        view_cart,
        name='view_cart'),
    path(
        'add/<int:item_id>/',
        add_to_cart,
        name='add_to_cart'),
    path(
        'delete/<int:item_id>/<str:size>/',
        delete_from_cart,
        name='delete_from_cart'),
]
