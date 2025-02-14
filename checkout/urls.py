from django.urls import path
from . import views

# URL patterns for checkout app
urlpatterns = [
    path('', views.checkout, name='checkout'),
    
]
