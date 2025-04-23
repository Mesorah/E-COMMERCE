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

    name = forms.CharField(
        max_length=55,
        widget=forms.TextInput(attrs={
            'placeholder': 'Nome do produto'
        })
    )

    price = forms.FloatField(
        widget=forms.NumberInput(attrs={
            'placeholder': 'Preço do produto'
        })
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Descrição do produto'
        })
    )

    stock = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'placeholder': 'Quantidade de estoque do produto'
        })
    )

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
            self.add_error(
                'price',
                'O valor do produto não pode ser menor ou igual a 0.'
            )

        return price

    def clean_stock(self):
        stock = self.cleaned_data['stock']

        if int(stock) < 0:
            self.add_error(
                'stock',
                'O valor do stock não pode ser menor que 0'
            )

        return stock


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
