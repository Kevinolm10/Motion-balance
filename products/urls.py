from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='all_products'),
    path('category/<slug:category_slug>/', views.product_category, name='product_category'),  # Updated to use one template
    path('sale/', views.sale_products, name='sale_products'),  # This will filter products that are on sale
    path('accessories/', views.all_accessories, name='all_accessories'),  # This will filter accessories
    path('subcategory/<slug:subcategory_slug>/', views.product_by_subcategory, name='product_by_subcategory'),
]
