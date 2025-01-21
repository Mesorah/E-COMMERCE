from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View

from home.forms import PaymentForm
from home.models import Cart, CartItem, Ordered, Products


class PaymentView(LoginRequiredMixin, View):
    login_url = reverse_lazy('authors:login')

    def get_itens(self):
        cart = Cart.objects.get(user=self.request.user)

        cart_item = CartItem.objects.filter(cart=cart, is_ordered=False)

        if not cart_item:
            raise ValueError("Carrinho vazio")

        return cart_item

    def get_render(self, form):
        return render(self.request, 'home/pages/payment.html', context={
         'form': form,
         'title': 'Payment'
        })

    def get_data(self, form):
        data = {
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'neighborhood': form.cleaned_data['neighborhood'],
                'street_name': form.cleaned_data['street_name'],
                'house_number': form.cleaned_data['house_number'],
            }

        return data

    def finalize_order(self, cart_item):
        for ct in cart_item.all():
            product = get_object_or_404(Products, name=ct.product)
            product.stock -= ct.quantity
            ct.is_ordered = True

            product.save()
            ct.save()

    def get(self, request):
        self.get_itens()

        form = PaymentForm()

        return self.get_render(form)

    def post(self, request):
        try:
            cart_item = self.get_itens()
        except ValueError:
            return redirect('home:index')

        form = PaymentForm(request.POST)

        if form.is_valid():

            products = cart_item.all()

            data = self.get_data(form)

            ordered = Ordered(**data)
            ordered.save()

            ordered.products.set(products)

            self.finalize_order(cart_item)

            return redirect('home:index')

        return self.get_render(form)
