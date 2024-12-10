from datetime import datetime

from creditcard import CreditCard
from django import forms


def validate_credit_card(card_number):
    card = CreditCard(card_number)

    if not card.is_valid:
        raise forms.ValidationError('Número de cartão de crédito inválido.')


class PaymentForm(forms.Form):
    firs_name = forms.CharField(max_length=50)
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
        max_length=5,
        widget=forms.TextInput(attrs={'placeholder': 'MM/AA'}),
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
    neighborhood = ...
    street_name = ...
    house_number = ...

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

            # Verifica se o ano é válido
            if year < datetime.now().year:
                raise forms.ValidationError("Ano de validade inválido.")
        except ValueError:
            raise forms.ValidationError("Formato de data inválido. Use MM/AA ou MM/YYYY.")

        return expiration_date
