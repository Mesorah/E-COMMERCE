from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View

from home.models import Cart, CartItem, Products


class AddToCartView(LoginRequiredMixin, View):
    login_url = reverse_lazy('authors:login')

    def get_itens(self, id):
        # Pega a quantidade no view_page, quando o usuário envia
        quantity = int(self.request.POST.get('quantity', 1))

        cart, _ = Cart.objects.get_or_create(user=self.request.user)

        product = get_object_or_404(Products, id=id)

        cart_item, _ = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': 0},
            is_ordered=False
        )

        return quantity, product, cart_item

    def post(self, request, id):
        quantity, product, cart_item = self.get_itens(id)

        if quantity > product.stock:
            messages.error(self.request,
                           'Não temos essa quantidade em estoque!'
                           )

            return redirect('home:view_page', pk=id)

        cart_item.quantity += quantity
        cart_item.save()

        return redirect('home:index')


class RemoveFromCartView(LoginRequiredMixin, View):
    login_url = reverse_lazy('authors:login')

    def get_itens(self, id):
        quantity = int(self.request.POST.get('quantity-to-remove', 1))

        cart, _ = Cart.objects.get_or_create(user=self.request.user)

        product = get_object_or_404(Products, id=id)

        cart_item, _ = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            is_ordered=False
        )

        return quantity, product, cart_item

    def post(self, request, id):
        quantity, product, cart_item = self.get_itens(id)

        product.stock += quantity
        product.save()

        cart_item.quantity -= quantity
        cart_item.save()

        return redirect('home:cart_detail')


class CartDetailView(View):
    def get_render(self, products, total_price):
        return render(self.request, 'home/pages/cart_detail.html', context={
            'title': 'Cart Detail',
            'products': products,
            'total_price': total_price
        })

    def get_item(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)

        cart_item = CartItem.objects.filter(
            cart=cart,
            is_ordered=False
        )

        products = cart_item.all()

        return products

    def get(self, request):
        products = self.get_item()

        total_price = 0

        for product in products:
            if product.quantity <= 0:
                product.delete()
                return redirect('home:cart_detail')

            total_price += product.product.price * product.quantity

        return self.get_render(products, total_price)
