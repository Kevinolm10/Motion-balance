from .models import Wishlist, WishlistItem

def wishlist_context(request):
    if request.user.is_authenticated:
        wishlist = Wishlist.objects.filter(user=request.user).first()
        wishlist_items = WishlistItem.objects.filter(wishlist=wishlist) if wishlist else []
        wishlist_product_ids = [item.product.id for item in wishlist_items]
    else:
        wishlist_items, wishlist_product_ids = [], []

    return {
        'wishlist_items': wishlist_items,
        'wishlist_product_ids': wishlist_product_ids,
    }
