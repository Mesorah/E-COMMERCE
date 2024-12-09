# from home.models import Cart


# def cart_item_count(request):
#     if request.user.is_authenticated:

#         cart = Cart.objects.filter(
#             user=request.user
#         ).first()

#         return {'cart_item_count': cart.products.count()}

#     return {'cart_item_count': 0}
