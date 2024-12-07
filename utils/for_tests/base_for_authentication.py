from django.contrib.auth.models import User
from authors.models import UserProfile


def register_user(username='Test', password='Test'):
    user = User.objects.create_user(
        username=username,
        password=password
    )

    return user


def register_user_profile(user, cpf='04887398026'):
    profile = UserProfile.objects.create(
        user=user,
        cpf=cpf
    )

    return profile


def register_super_user(
        username='test',
        email='test@example.com',
        password='123'
     ):

    profile = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )

    return profile
