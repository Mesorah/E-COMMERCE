from django import forms

from home.models import Products


class CrudProduct(forms.ModelForm):
    class Meta:
        model = Products
        fields = [
            'name',
            'price',
            'description',
            'stock',
            'is_published',
            'cover'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_name(self):
        name = self.cleaned_data['name']

        if len(name) <= 2:
            self.add_error('name',
                           """Nome de produto muito pequeno,
                           precisa-se de pelo menos 3 caracteres"""
                           )

        return name

    def clean_price(self):
        price = self.cleaned_data['price']

        if int(price) <= 0:
            self.add_error('price',
                           'O valor do produto nãopode ser menor ou igual a 0.'
                           )

        return price


class SupportStaffForm(forms.Form):
    email = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'id': 'email',
                'name': 'email',
                'rows': 5,
                'required': True,
                'placeholder': 'Escreva o email aqui...',
                'class': 'form-label'
            }
        ),
        label="E-mail:"
    )
    answer = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'id': 'answer',
                'name': 'answer',
                'rows': 5,
                'required': True,
                'placeholder': 'Escreva sua resposta aqui...',
                'class': 'form-label'
            }
        ),
        label="Resposta:"
    )
