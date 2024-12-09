from home.models import Products, Cart, CartItem
from django.http import Http404
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect, get_object_or_404


class HomeListView(ListView):
    template_name = 'global/pages/base_page.html'
    model = Products
    context_object_name = 'products'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)

        queryset = queryset.filter(
            is_published=True
        )

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context.update({
            'title': 'Home',
        })

        return context


class PageDetailView(DetailView):
    template_name = 'home/pages/view_page.html'
    model = Products
    context_object_name = 'product'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)

        queryset = queryset.filter(
            pk=self.kwargs.get('pk'),
            is_published=True
        )

        if not queryset:
            raise Http404()

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        product = self.get_object()

        cart_item = CartItem.objects.filter(
            cart=self.kwargs.get('pk'),
            product=product,
        ).first()

        context.update({
            'title': 'View Page',
            'stock': product.stock,
            'have_produtct': cart_item
        })

        return context


def add_to_cart(request, id):
    cart, _ = Cart.objects.get_or_create(user=request.user)

    product = get_object_or_404(Products, id=id)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 0}
    )

    cart_item.add_quatity(1) # passar a quantidade

    return redirect('home:index')


def remove_from_cart(request, id):
    cart = Cart.objects.filter(
        user=request.user
    ).first()

    if not cart:
        return redirect('home:index')

    cart.products.remove(id)

    return redirect('home:cart_detail')


def cart_detail_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)

    product = get_object_or_404(Products, id=id)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 0}
    )

    products = cart_item.product.all()
    total_price = 0

    for produt in products:
        total_price += produt.price

    return render(request, 'home/pages/cart_detail.html', context={
        'products': '',
        'total_price': 150
    })

# No comprar produtos a hora que
# a pessoa for digitar o cep
# se for diferentes da que eu
# colocar permitido dar um erro
