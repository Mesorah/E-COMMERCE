from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View

from authors.models import UserProfile
from home.forms import PaymentForm
from home.models import CartItem, Ordered, Products


class PaymentView(LoginRequiredMixin, View):
    login_url = reverse_lazy('authors:login')

    def set_stock_products(self, cart_item):
        products = []
        for i, item in enumerate(cart_item):
            item.product.stock -= item.quantity
            products.append(item.product)

        Products.objects.bulk_update(products, ['stock'])

    def get_items(self):
        cart = self.request.session.get('cart', {})

        items = []
        for value in cart.values():
            product_id = value['product']['id']
            quantity = value['quantity']
            items.append((product_id, quantity))

        # ordena os itens pelo primeiro elemento da tupla (o product_id)
        items.sort(key=lambda item: item[0])

        product_ids = []
        products_quantity = []
        for item in items:
            product_ids.append(item[0])         # product_id
            products_quantity.append(item[1])   # quantity

        products = Products.objects.filter(pk__in=product_ids).order_by('pk')

        return products, products_quantity

    def create_cart_items(self, products, products_quantity):
        cart_items = []
        user_profile = UserProfile.objects.filter(
            user=self.request.user
        ).first()

        for i, product in enumerate(products):
            item = CartItem(
                product=product,
                user=user_profile,
                quantity=products_quantity[i]
            )

            cart_items.append(item)

        CartItem.objects.bulk_create(cart_items)

        return cart_items

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

    def get(self, *args, **kwargs):
        form = PaymentForm()
        cart = self.request.session.get('cart', {})

        if not cart:
            messages.error(self.request, 'Nenhum item no carrinho.')
            return redirect('home:index')

        return self.get_render(form)

    def post(self, *args, **kwargs):
        products, products_quantity = self.get_items()

        form = PaymentForm(self.request.POST)

        if form.is_valid():
            data = self.get_data(form)

            cart_items = self.create_cart_items(products, products_quantity)

            ordered = Ordered(**data)
            ordered.save()

            ordered.products.add(*cart_items)

            self.request.session['cart'] = {}
            self.request.session.modified = True

            self.set_stock_products(cart_items)

            return redirect('home:index')

        return self.get_render(form)
