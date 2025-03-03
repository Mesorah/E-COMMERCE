def cart_item_count(request):
    if request.user.is_authenticated:
        try:
            cart = request.session['cart']
        except KeyError:
            return {'cart_item_count': 0}

        return {'cart_item_count': len(cart)}

    return {'cart_item_count': 0}
