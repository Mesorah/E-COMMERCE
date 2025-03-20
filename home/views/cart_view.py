import uuid

from django.conf import settings
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View

from home.models import Products


class CartView(View):
    login_url = reverse_lazy('authors:login')

    def init_cart(self):
        cart = self.request.session.get('cart')

        if not cart:
            self.request.session['cart'] = {}

        self.id_variation = str(uuid.uuid4())

        return cart

    def find_product_in_cart(self, cart, product, quantity, sum=True):
        product_name = product.get('name')

        if cart:
            for k, v in cart.items():
                if v['product']['name'] == product_name:

                    if sum:
                        v['quantity'] += quantity
                    else:
                        v['quantity'] -= quantity

                    self.request.session.modified = True

                    return k

            # Se o produto não estiver na session
            # ou seja, um novo produto
            return False

    def get_item(self, pk):
        cart = self.init_cart()

        quantity = int(self.request.POST.get('quantity', 1))
        product = get_object_or_404(Products, pk=pk)

        # Dados para apenas MOSTRAR para o usuário
        product = {
            'id': product.pk,
            'cover': product.cover,
            'name': product.name,
            'slug': product.slug,
            'stock': product.stock,
            'price': product.price
        }

        product['cover'] = str(product['cover'])

        return cart, quantity, product

    def set_itens(self, quantity, product):
        self.request.session['cart'][self.id_variation] = {
            'quantity': quantity,
            'product': product
        }

        self.request.session.modified = True

        return self.request.session['cart'][self.id_variation]

    def get_items(self, session_cart):
        items = []
        for k, value in session_cart.items():
            quantity = value['quantity']
            id = value['product']['id']
            items.append((id, quantity))

        return items

    def get_session_quantity(self, items, pk):
        session_quantity = 0
        for item in items:
            # id
            if item[0] == pk:
                session_quantity = item[1]

        return session_quantity

    def post(self, *args, **kwargs):
        cart, quantity, product = self.get_item(
            self.kwargs.get('pk')
        )

        has_product = self.find_product_in_cart(cart, product, quantity)
        if not has_product:
            self.set_itens(quantity, product)

        session_cart = self.request.session['cart']
        items = self.get_items(session_cart)
        pk = self.kwargs.get('pk')
        session_quantity = self.get_session_quantity(items, pk)

        if quantity > product['stock'] or session_quantity > product['stock']:
            self.find_product_in_cart(cart, product, quantity, False)

            messages.error(self.request,
                           'Não temos essa quantidade em estoque!'
                           )

            return redirect('home:view_page', slug=product['slug'])

        return redirect('home:index')


class AddToCartView(CartView):
    pass


class RemoveFromCartView(CartView):
    login_url = reverse_lazy('authors:login')

    def post(self, *args, **kwargs):
        quantity = int(self.request.POST.get('quantity-to-remove', 1))
        cart, _, product = self.get_item(self.kwargs.get('pk'))

        self.find_product_in_cart(
            cart, product, quantity, False
        )

        product['stock'] -= quantity

        self.request.session.modified = True

        return redirect('home:cart_detail')


class CartDetailView(View):
    login_url = reverse_lazy('authors:login')

    def get_render(self, products=None, total_price=0):
        return render(self.request, 'home/pages/cart_detail.html', context={
            'title': 'Cart Detail',
            'products': products,
            'total_price': total_price,
            'MEDIA_URL': settings.MEDIA_URL,
        })

    def is_quantity_zero_or_less(self, products):
        total_price = 0

        product_to_remove = []

        for k, v in products.items():
            if int(v['quantity']) <= 0:
                product_to_remove.append(k)

            total_price += int(v['product']['price']) * int(v['quantity'])

        for k in product_to_remove:
            del self.request.session['cart'][k]

        self.request.session.modified = True

        return total_price

    def get(self, request):
        products = self.request.session.get('cart')

        total_price = 0

        if products:
            total_price = self.is_quantity_zero_or_less(products)

        return self.get_render(products, total_price)
