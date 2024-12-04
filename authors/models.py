from django.db import models
from django.contrib.auth.models import User
from validate_docbr import CPF


def validate_cpf(value):
    cpf = CPF()
    if not cpf.validate(value):
        raise models.ValidationError('CPF inválido.')


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cpf = models.CharField(
        max_length=11,
        unique=True,
        validators=[validate_cpf]
    )

    def __str__(self):
        return f'{self.user.username} - {self.cpf}'
