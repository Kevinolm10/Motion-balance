from django.urls import path
from . import views

# URL patterns for user_profile app
urlpatterns = [
    path('profile/', views.user_profile, name='user_profile'),  # User profile
]
