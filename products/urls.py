from django.urls import path
from . import views

# URL patterns for products app
urlpatterns = [
    path('', views.all_products, name='all_products'),
    path('category/<slug:category_slug>/', views.product_category, name='product_category'),
    path('sale/', views.sale_products, name='sale_products'),
    path('accessories/', views.all_accessories, name='all_accessories'),
    path('subcategory/<slug:subcategory_slug>/', views.product_by_subcategory, name='product_by_subcategory'),
]