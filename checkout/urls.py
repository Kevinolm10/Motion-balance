from django.urls import path
from . import views

# URL patterns for checkout app
urlpatterns = [
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('checkout/', views.checkout, name='checkout'),  # Add this line
]
