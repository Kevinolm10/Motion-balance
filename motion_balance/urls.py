from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('home.urls')),
    path('products/', include('products.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('checkout/', include('checkout.urls')),  # Include the checkout app URLs
    path('cart/', include('cart.urls')),  # Include the cart app URLs
    path('user_profile/', include('user_profile.urls')),  # Ensure the trailing slash
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)