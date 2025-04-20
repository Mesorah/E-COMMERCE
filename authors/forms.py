from django import forms
from django.contrib.auth.forms import UserCreationForm
from validate_docbr import CPF

from authors.models import UserProfile


def validate_cpf(value):
    cpf = CPF()
    if not cpf.validate(value):
        raise forms.ValidationError('CPF inválido.')


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': 'Ex.: Gabriel'
        }
    ))

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Ex.: exemplo@email.com',
            }
        )
    )

    cpf = forms.CharField(
        min_length=11,
        max_length=11,
        required=True,
        validators=[validate_cpf],
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Ex.: 32470317070'
            }
        )
    )

    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Ex.: y897`YuA/u/e',
            }
        )
    )

    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Ex.: y897`YuA/u/e',
            }
        )
    )

    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'cpf', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_username(self):
        username = self.cleaned_data['username']

        if len(username.strip()) < 3:
            raise forms.ValidationError(
                "Nome precisa de pelo menos 3 caracteres"
            )

        return username
