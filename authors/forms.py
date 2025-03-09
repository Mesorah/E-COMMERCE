from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from validate_docbr import CPF

from authors.models import UserProfile


def validate_cpf(value):
    cpf = CPF()
    if not cpf.validate(value):
        raise forms.ValidationError('CPF inválido.')


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    cpf = forms.CharField(
        min_length=11,
        max_length=11,
        required=True,
        validators=[validate_cpf]
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'cpf', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            user.save()

            profile = UserProfile(user=user, cpf=self.cleaned_data['cpf'])
            profile.save()

        return user
