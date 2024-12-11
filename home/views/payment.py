from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from home.forms import PaymentForm
from home.models import Cart, CartItem, Ordered


@login_required()
def payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)

        if form.is_valid():
            cart, _ = Cart.objects.get_or_create(user=request.user)

            cart_item = CartItem.objects.filter(
                cart=cart,
            )

            products = cart_item.all()

            data = {
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'street_name': form.cleaned_data['street_name'],
                'house_number': form.cleaned_data['house_number'],
            }

            ordered = Ordered(**data)
            ordered.save()
            ordered.products.set(products)

            return redirect('home:index')

    else:
        form = PaymentForm()

    return render(request, 'home/pages/payment.html', context={
        'form': form
    })
