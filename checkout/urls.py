from django.urls import path
from . import views
from .webhooks import webhook


"""  Checkout URLs  """
urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('checkout_success/<str:order_number>/', views.checkout_success, name='checkout_success'),
    path(
        'cache_checkout_data/',
        views.cache_checkout_data,
        name='cache_checkout_data'),
    path(
        'order/<int:order_id>/',
        views.order_detail,
        name='order_detail'),
    path('wh/', webhook, name='webhook'),
]
