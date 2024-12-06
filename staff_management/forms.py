from django import forms
from home.models import Products


class AddProduct(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['name', 'price', 'description', 'cover']
