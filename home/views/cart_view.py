from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View

from home.models import Products


class AddToCartView(LoginRequiredMixin, View):
    login_url = reverse_lazy('authors:login')

    def set_max_id_variation(self, cart):
        self.id_variation = 0
        for product in cart:
            self.id_variation = max(self.id_variation, int(product))

        return self.id_variation

    def init_cart(self):
        cart = self.request.session.get('cart')

        if not cart:
            self.request.session['cart'] = {}
            self.id_variation = 0
        else:
            self.set_max_id_variation(cart)

        return cart

    def verify_if_has_exist(self, cart, product, quantity):
        product_name = product.get('name')

        if cart:
            for k, v in cart.items():
                if v['product']['name'] == product_name:
                    v['quantity'] += quantity

                    self.request.session.modified = True

                    return cart

            # Se o produto não estiver na session
            # ou seja, um novo produto
            return False

    def get_itens(self, id):
        cart = self.init_cart()
        self.id_variation += 1

        quantity = int(self.request.POST.get('quantity', 1))
        product = get_object_or_404(Products, id=id)

        product = model_to_dict(product)
        product['cover'] = str(product['cover'])

        return cart, quantity, product

    def set_itens(self, quantity, product):
        self.request.session['cart'][self.id_variation] = {
            'quantity': quantity,
            'product': product
        }

        self.request.session.modified = True

        return self.request.session['cart'][self.id_variation]

    def post(self, request, id, *args, **kwargs):
        cart, quantity, product = self.get_itens(id)

        if quantity > product['stock']:
            messages.error(self.request,
                           'Não temos essa quantidade em estoque!'
                           )

            return redirect('home:view_page', slug=product['slug'])

        has_product = self.verify_if_has_exist(cart, product, quantity)

        if not has_product:
            self.set_itens(quantity, product)

        print(self.request.session['cart'])

        return redirect('home:index')


# class AddToCartView(LoginRequiredMixin, View):
#     login_url = reverse_lazy('authors:login')

#     def get_itens(self, id):
#         # Pega a quantidade no view_page, quando o usuário envia
#         quantity = int(self.request.POST.get('quantity', 1))

#         cart = Cart.objects.get(user=self.request.user)

#         product = get_object_or_404(Products, id=id)

#         cart_item, _ = CartItem.objects.get_or_create(
#             cart=cart,
#             product=product,
#             defaults={'quantity': 0},
#             is_ordered=False
#         )

#         return quantity, product, cart_item

#     def post(self, request, id):
#         quantity, product, cart_item = self.get_itens(id)

#         if cart_item.quantity >= product.stock or quantity > product.stock:
#             messages.error(self.request,
#                            'Não temos essa quantidade em estoque!'
#                            )

#             return redirect('home:view_page', slug=product.slug)

#         cart_item.quantity += quantity
#         cart_item.save()

#         return redirect('home:index')


class RemoveFromCartView(AddToCartView):
    login_url = reverse_lazy('authors:login')

    def post(self, request, id, *args, **kwargs):
        self.get_itens(id)
        quantity = int(self.request.POST.get('quantity-to-remove', 1))

        # usando o -1 pois o self.get_itens adiciona +1 no
        # self.id_variation
        product = self.request.session['cart'][str(self.id_variation-1)]
        product['quantity'] -= quantity

        self.request.session.modified = True

        print(self.request.session['cart'])

        return redirect('home:cart_detail')


# class RemoveFromCartView(LoginRequiredMixin, View):
#     login_url = reverse_lazy('authors:login')

#     def get_itens(self, id):
#         quantity = int(self.request.POST.get('quantity-to-remove', 1))

#         cart = Cart.objects.get(user=self.request.user)

#         product = get_object_or_404(Products, id=id)

#         cart_item, _ = CartItem.objects.get_or_create(
#             cart=cart,
#             product=product,
#             is_ordered=False
#         )

#         return quantity, product, cart_item

#     def post(self, request, id):
#         quantity, product, cart_item = self.get_itens(id)

#         product.stock += quantity
#         product.save()

#         cart_item.quantity -= quantity

#         if cart_item.quantity <= 0:
#             cart_item.delete()
#         else:
#             cart_item.save()

#         return redirect('home:cart_detail')


class CartDetailView(LoginRequiredMixin, View):
    login_url = reverse_lazy('authors:login')

    def get_render(self, products=None, total_price=0):
        return render(self.request, 'home/pages/cart_detail.html', context={
            'title': 'Cart Detail',
            'products': products,
            'total_price': total_price
        })

    def is_quantity_zero_or_less(self, products):
        total_price = 0

        for k, v in products.items():
            if int(v['quantity']) <= 0:
                del self.request.session['cart'][k]

                self.request.session.modified = True

                return total_price

            total_price += int(v['product']['price']) * int(v['quantity'])

        return total_price

    def get(self, request):
        products = self.request.session.get('cart')

        total_price = self.is_quantity_zero_or_less(products)

        return self.get_render(products, total_price)

# class CartDetailView(LoginRequiredMixin, View):
#     login_url = reverse_lazy('authors:login')

#     def get_render(self, products=None, total_price=0):
#         return render(self.request, 'home/pages/cart_detail.html', context={
#             'title': 'Cart Detail',
#             'products': products,
#             'total_price': total_price
#         })

#     def get_item(self):
#         cart = Cart.objects.get(user=self.request.user)

#         cart_item = CartItem.objects.filter(
#             cart=cart,
#             is_ordered=False
#         )

#         products = cart_item.all()

#         return products

#     def get(self, request):
#         products = self.get_item()

#         total_price = 0

#         for product in products:
#             if product.quantity <= 0:
#                 product.delete()
#                 return redirect('home:cart_detail')

#             total_price += product.product.price * product.quantity

#         return self.get_render(products, total_price)
