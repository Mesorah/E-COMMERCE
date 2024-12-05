from home.models import Products


def create_product(user, name='Test Product', price=150, description='Test'):
    product = Products.objects.create(
            name=name,
            price=price,
            description=description,
            user=user
        )

    return product
