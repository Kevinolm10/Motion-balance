from django.contrib import admin
from django.urls import path
from . import views

"""  Home URLs  """
urlpatterns = [
    path('', views.index, name='home')
]
