from django.urls import path
from . import views

# URL patterns for orders app
urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
]