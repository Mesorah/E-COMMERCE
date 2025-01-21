from home.models import Cart, CartItem


def cart_item_count(request):
    if request.user.is_authenticated:

        cart = Cart.objects.filter(user=request.user).first()

        cart_item = CartItem.objects.filter(
            cart=cart,
            is_ordered=False
        )

        return {'cart_item_count': cart_item.count()}

    return {'cart_item_count': 0}
