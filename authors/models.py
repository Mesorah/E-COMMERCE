from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from validate_docbr import CPF


def validate_cpf(value):
    cpf = CPF()
    if not cpf.validate(value):
        raise ValidationError('CPF inválido.')


class UserProfile(AbstractUser):
    cpf = models.CharField(
        max_length=11,
        unique=True,
        validators=[validate_cpf]
    )

    def __str__(self):
        return f'{self.username} - {self.cpf}'
