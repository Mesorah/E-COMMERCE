from creditcard import CreditCard
from django import forms


def validate_credit_card(card_number):
    card = CreditCard(card_number)

    if not card.is_valid(card_number):
        raise forms.ValidationError('CPF inválido.')


class PaymentForm(forms.Form):
    name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    credit_card = forms.CharField(
        max_length=16,
        widget=forms.TextInput(attrs={
            'placeholder': 'Número do cartão de crédito'
        }),
        validators=[validate_credit_card]
    )
    expiration_date = forms.CharField(
        max_length=5,
        widget=forms.TextInput(attrs={'placeholder': 'MM/AAAA'}),
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

    def clean_expiration_date(self):
        expiration_date = self.cleaned_data['expiration_date']
        try:
            month, year = expiration_date.split('/')
            month = int(month)
            year = int(year)
            if month < 1 or month > 12:
                raise forms.ValidationError("Mês inválido.")
            if year < 2024:
                raise forms.ValidationError("Ano de validade inválido.")
        except ValueError:
            raise forms.ValidationError(
                "Formato de data inválido. Use MM/AAAA."
            )

        return expiration_date
