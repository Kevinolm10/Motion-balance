from django.urls import path
from .views import UserProfileView, UserProfileEditView

urlpatterns = [
    path('', UserProfileView.as_view(), name='profile'),  # View user profile
    path('edit/', UserProfileEditView.as_view(), name='profile-edit'),  # Edit user profile
]
