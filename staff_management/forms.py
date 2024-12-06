from django import forms
from home.models import Products


class CrudProduct(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['name', 'price', 'description', 'cover']
