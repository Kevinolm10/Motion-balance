from django import forms
from .models import ProductFeedback

from django import forms
from .models import Product

class ProductFilterForm(forms.Form):
    min_price = forms.DecimalField(required=False, decimal_places=2, max_digits=10, label='Min Price')
    max_price = forms.DecimalField(required=False, decimal_places=2, max_digits=10, label='Max Price')
    min_discount = forms.DecimalField(required=False, decimal_places=2, max_digits=5, label='Min Discount')
    max_discount = forms.DecimalField(required=False, decimal_places=2, max_digits=5, label='Max Discount')
    min_rating = forms.DecimalField(required=False, decimal_places=1, max_digits=2, label='Min Rating')
    max_rating = forms.DecimalField(required=False, decimal_places=1, max_digits=2, label='Max Rating')

    def filter_products(self, queryset):
        """
        Apply filters to a given queryset of products.
        """
        if self.is_valid():
            if self.cleaned_data['min_price']:
                queryset = queryset.filter(price__gte=self.cleaned_data['min_price'])
            if self.cleaned_data['max_price']:
                queryset = queryset.filter(price__lte=self.cleaned_data['max_price'])
            if self.cleaned_data['min_discount']:
                queryset = queryset.filter(discount_percentage__gte=self.cleaned_data['min_discount'])
            if self.cleaned_data['max_discount']:
                queryset = queryset.filter(discount_percentage__lte=self.cleaned_data['max_discount'])
            if self.cleaned_data['min_rating']:
                queryset = queryset.filter(average_rating__gte=self.cleaned_data['min_rating'])
            if self.cleaned_data['max_rating']:
                queryset = queryset.filter(average_rating__lte=self.cleaned_data['max_rating'])
        return queryset


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = ProductFeedback
        fields = ['rating', 'comment']