from home.models import CartItem
from utils.for_tests.base_for_authentication import (  # noqa E501
    register_super_user,
    register_user,
)
from utils.for_tests.base_for_create_itens import (
    create_cart,
    create_cart_item,
    create_ordered,
    create_product,
)


def create_cart_item_setup():
    user = register_user()
    # client.login(username='Test', password='Test')

    product = create_product(user)
    cart = create_cart(user)
    cart_item = create_cart_item(cart, product)

    return cart_item


def create_ordered_setup():
    user = register_super_user()

    product = create_product(user)
    cart = create_cart(user)
    cart_item = create_cart_item(cart, product)
    cart_item = CartItem.objects.filter(cart=cart, is_ordered=False)
    ordered = create_ordered()
    ordered.products.set(cart_item)

    return ordered
