from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='all_products'),
    path('products/category/<slug:category_slug>/', views.product_category, name='product_category'),
    path('sale/', views.sale_products, name='sale_products'),
    path('sale/category/<slug:category_slug>/', views.sale_category, name='sale_category'),
    path('accessories/', views.all_accessories, name='all_accessories'),
]
