from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import handler404, handler500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('home.urls')),
    path('products/', include('products.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('checkout/', include('checkout.urls')),
    path('cart/', include('cart.urls')),
    path('user_profile/', include('user_profile.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'motion_balance.views.handler404'
handler500 = 'motion_balance.views.handler500'
