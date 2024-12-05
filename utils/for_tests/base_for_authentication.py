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
