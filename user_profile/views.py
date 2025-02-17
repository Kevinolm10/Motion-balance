from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import UserProfile
from .forms import UserProfileForm
from checkout.models import Order
from products.models import ProductFeedback
from wishlist.models import WishlistItem


""" View for the user profile page. """


def user_profile(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=request.user)
        profile.save()
    """ Update the user profile. """
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(
                    request, 'Your profile has been updated successfully.')
            return redirect('user_profile')
    else:
        form = UserProfileForm(instance=profile)

    orders = Order.objects.filter(user=request.user)
    feedbacks = ProductFeedback.objects.filter(user=request.user)
    wishlist_items = WishlistItem.objects.filter(wishlist__user=request.user)

    """ Render the user profile template. """
    return render(request, 'user_profile/user_profile.html', {
        'form': form,
        'orders': orders,
        'feedbacks': feedbacks,
        'wishlist_items': wishlist_items,
    })
