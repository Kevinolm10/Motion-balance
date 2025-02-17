from django.urls import path
from . import views


"""  User Profile URLs  """
urlpatterns = [
    path('profile/', views.user_profile, name='user_profile'),
]
