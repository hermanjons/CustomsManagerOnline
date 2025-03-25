from django import forms
from .models import Brand


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['brand_name', 'brand_code', 'brand_activate_number', 'brand_description', 'activated_countries',
                  'brand_logo']
