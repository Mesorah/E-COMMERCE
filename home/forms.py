from datetime import datetime

from creditcard import CreditCard
from django import forms


def validate_credit_card(card_number):
    card = CreditCard(card_number)

    if not card.is_valid:
        raise forms.ValidationError('Número de cartão de crédito inválido.')


class PaymentForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    credit_card = forms.CharField(
        max_length=16,
        widget=forms.TextInput(attrs={
            'placeholder': 'Número do cartão de crédito'
        }),
        required=True,
        validators=[validate_credit_card],
    )
    expiration_date = forms.CharField(
        max_length=7,
        widget=forms.TextInput(attrs={'placeholder': 'MM/AA ou MM/YYYY'}),
    )
    cvv = forms.CharField(
        max_length=4,
        widget=forms.TextInput(attrs={'placeholder': 'CVV'}),
    )
    cardholder_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Nome do titular do cartão'
        }),
    )
    zip_code = forms.CharField(
        max_length=8,
        min_length=8,
        widget=forms.TextInput(attrs={
            'placeholder': 'XXXXXXXX'
        }),
    )
    neighborhood = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Bairo'
        }),
    )
    street_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Rua'
        }),
    )
    house_number = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={
            'placeholder': 'Número da casa'
        }),
    )

    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_expiration_date(self):
        expiration_date = self.cleaned_data['expiration_date']
        try:
            parts = expiration_date.split('/')
            if len(parts) != 2:
                raise forms.ValidationError(
                    "Formato de data inválido. Use MM/AA ou MM/YYYY."
                )

            month, year = parts
            month = int(month)

            if month < 1 or month > 12:
                raise forms.ValidationError("Mês inválido.")

            if len(year) == 2:
                year = '20' + year
            year = int(year)

            if year < datetime.now().year:
                raise forms.ValidationError("Ano de validade inválido.")

            return f'{month:02d}/{year}'

        except ValueError:
            raise forms.ValidationError(
                "Formato de data inválido. Use MM/AA ou MM/YYYY."
            )

        # return expiration_date

    def clean_zip_code(self):
        zip_code = self.cleaned_data['zip_code']

        allowed_zip_codes = [
            '86390000'
        ]

        if zip_code not in allowed_zip_codes:
            raise forms.ValidationError("CEP diferente de cambará")

        return zip_code
