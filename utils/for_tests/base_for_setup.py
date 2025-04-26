from home.models import CartItem
from utils.for_tests.base_for_authentication import (  # noqa E501
    register_super_user,
    register_user,
)
from utils.for_tests.base_for_create_itens import (
    create_cart_item,
    create_ordered,
    create_product,
)


def create_cart_item_setup(staff=False, product_2=False, stock1=1, stock2=1):
    if staff:
        user = register_super_user()
    else:
        user = register_user()

    product = create_product(user, stock1)
    cart_item = create_cart_item(product, user)

    if product_2:
        product_2 = create_product(user, stock2, name='teste product 2')
        cart_item2 = create_cart_item(product_2, user)

        return product, product_2, cart_item, cart_item2, user

    return product, cart_item


def create_ordered_setup(user=False, qtd=1):
    if not user:
        user = register_super_user()

    product = create_product(user)

    cart_item = create_cart_item(product, user)
    cart_item = CartItem.objects.filter(user=user)

    for i in range(qtd):
        ordered = create_ordered(first_name=f'Test-{qtd}', last_name='')
        ordered.products.set(cart_item)

    return ordered


def create_product_setup(
        qtd=1, super_user_profile=None,
        username='test', password='123',
        return_super_user=False
):
    if super_user_profile is None:
        super_user_profile = register_super_user(username, password)

    for i in range(qtd):
        product = create_product(super_user_profile, name=f'Product-{i}')

    if return_super_user:
        return super_user_profile

    return product
