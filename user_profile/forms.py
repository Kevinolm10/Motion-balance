from django import forms
from .models import UserProfile


""" Form for updating user profile. """


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'address', 'phone_number']
