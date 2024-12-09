from home.models import Products, Cart, CartItem


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


def create_cart(user):
    cart = Cart.objects.create(user=user)

    return cart


def create_cart_item(cart, product, quantity=1):
    cart_item = CartItem.objects.create(
        cart=cart,
        product=product,
        quantity=quantity
    )

    return cart_item
