from home.models import Products


def create_product(
        user,
        name='Test Product',
        price=150,
        description='Test',
        stock=1,
        is_published=True
        ):
    product = Products.objects.create(
            name=name,
            price=price,
            description=description,
            stock=stock,
            is_published=is_published,
            user=user,
        )

    return product
