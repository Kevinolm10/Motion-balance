from django.urls import path
from .views import WishlistView, WishlistAddView, WishlistRemoveView

urlpatterns = [
    path('', WishlistView.as_view(), name='wishlist'),  # View wishlist
    path('add/<int:product_id>/', WishlistAddView.as_view(), name='wishlist-add'),  # Add to wishlist
    path('remove/<int:product_id>/', WishlistRemoveView.as_view(), name='wishlist-remove'),  # Remove from wishlist
]
