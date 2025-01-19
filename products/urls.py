from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='all_products'),
    path('products/category/<slug:category_slug>/', views.product_category, name='product_category'),
]