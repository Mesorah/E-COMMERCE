from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from home.forms import PaymentForm
from home.models import Cart, CartItem, Ordered, Products


@login_required(login_url='authors:login')
# No comprar produtos a hora que
# a pessoa for digitar o cep
# se for diferentes da que eu
# colocar permitido dar um erro
def payment(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)

    cart_item = CartItem.objects.filter(cart=cart, is_ordered=False)

    if not cart_item:
        return redirect('home:index')

    if request.method == 'POST':
        form = PaymentForm(request.POST)

        if form.is_valid():

            products = cart_item.all()

            data = {
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'neighborhood': form.cleaned_data['neighborhood'],
                'street_name': form.cleaned_data['street_name'],
                'house_number': form.cleaned_data['house_number'],
            }

            ordered = Ordered(**data)
            ordered.save()

            ordered.products.set(products)

            for ct in cart_item.all():
                product = get_object_or_404(Products, name=ct.product)
                product.stock -= ct.quantity
                ct.is_ordered = True

                product.save()
                ct.save()

            return redirect('home:index')

    else:
        form = PaymentForm()

    return render(request, 'home/pages/payment.html', context={
        'form': form
    })
