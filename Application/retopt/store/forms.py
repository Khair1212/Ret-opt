from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'product_cat', 'product_cat_code', 'product_subcat', 'product_subcat_code', 'price', 'image']