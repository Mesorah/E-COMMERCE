from django import forms
from home.models import Products


class CrudProduct(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['name', 'price', 'description', 'cover']

    def clean_name(self):
        name = self.cleaned_data['name']

        if len(name) <= 2:
            self.add_error('name',
                           """Nome de produto muito pequeno,
                           precisa-se de pelo menos 3 caracteres"""
                           )

    def clean_price(self):
        price = self.cleaned_data['price']

        if int(price) <= 0:
            self.add_error('price',
                           'o valor do produto não pode ser menor ou igual a 0'
                           )
