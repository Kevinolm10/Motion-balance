
from django.urls import path
from . import views

# URL patterns for products app
urlpatterns = [
    path('', views.all_products, name='all_products'),
    path('product/<int:product_id>/', views.product_details, name='product_details'),
    path('category/<slug:category_slug>/', views.product_category, name='product_category'),
    path('sale/', views.sale_products, name='sale_products'),
    path('accessories/', views.all_accessories, name='all_accessories'),
    path('subcategory/<slug:subcategory_slug>/', views.product_by_subcategory, name='product_by_subcategory'),
    path('<int:product_id>/feedback/create/', views.create_feedback, name='create_feedback'),
    path('feedback/<int:feedback_id>/update/', views.update_feedback, name='update_feedback'),
    path('feedback/<int:feedback_id>/delete/', views.delete_feedback, name='delete_feedback'),
    path('add_to_wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_from_wishlist/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
]
