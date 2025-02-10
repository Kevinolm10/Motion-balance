from django import forms
from .models import ProductFeedback

class ProductFilterForm(forms.Form):
    min_price = forms.DecimalField(required=False, decimal_places=2, max_digits=10, label='Min Price')
    max_price = forms.DecimalField(required=False, decimal_places=2, max_digits=10, label='Max Price')
    min_discount = forms.DecimalField(required=False, decimal_places=2, max_digits=5, label='Min Discount')
    max_discount = forms.DecimalField(required=False, decimal_places=2, max_digits=5, label='Max Discount')
    min_rating = forms.DecimalField(required=False, decimal_places=1, max_digits=2, label='Min Rating')
    max_rating = forms.DecimalField(required=False, decimal_places=1, max_digits=2, label='Max Rating')

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = ProductFeedback
        fields = ['rating', 'comment']