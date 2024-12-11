from home.models import Cart, CartItem


def cart_item_count(request):
    if request.user.is_authenticated:

        cart, _ = Cart.objects.get_or_create(user=request.user)

        cart_item = CartItem.objects.filter(
            cart=cart,
            is_ordered=False
        )

        return {'cart_item_count': cart_item.count()}

    return {'cart_item_count': 0}
