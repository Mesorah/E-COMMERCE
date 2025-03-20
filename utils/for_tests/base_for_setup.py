from home.models import CartItem
from utils.for_tests.base_for_authentication import (  # noqa E501
    register_super_user,
    register_user,
    register_user_profile,
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

    user_profile = register_user_profile(user)

    product = create_product(user, stock1)
    cart_item = create_cart_item(product, user_profile)

    if product_2:
        product_2 = create_product(user, stock2, name='teste product 2')
        cart_item2 = create_cart_item(product_2, user_profile)

        return product, product_2, cart_item, cart_item2, user_profile

    return product, cart_item


def create_ordered_setup():
    user = register_super_user()

    product = create_product(user)

    user_profile = register_user_profile(user)

    cart_item = create_cart_item(product, user_profile)
    cart_item = CartItem.objects.filter(user=user_profile)
    ordered = create_ordered()
    ordered.products.set(cart_item)

    return ordered
