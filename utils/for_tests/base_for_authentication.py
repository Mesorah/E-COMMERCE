from authors.models import UserProfile


def register_user(
        username='Test',
        password='Test',
        cpf='21257890000'
     ):
    user = UserProfile.objects.create_user(
        username=username,
        password=password,
        cpf=cpf
    )

    return user


def register_super_user(
        username='test',
        email='test@example.com',
        password='123',
        cpf='04887398026'
     ):

    profile = UserProfile.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            cpf=cpf
        )

    return profile
