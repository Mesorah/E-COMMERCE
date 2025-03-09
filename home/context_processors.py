def cart_item_count(request):
    try:
        cart = request.session['cart']
    except KeyError:
        return {'cart_item_count': 0}

    return {'cart_item_count': len(cart)}
