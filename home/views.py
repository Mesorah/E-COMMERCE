from django.shortcuts import render, redirect, get_object_or_404
from home.models import Products, Cart, CartItem
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.http import Http404


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
    if request.method == 'POST':
        # Pega a quantidade no view_page, quando o usuário envia
        quantity = int(request.POST.get('quantity', 1))

        cart, _ = Cart.objects.get_or_create(user=request.user)

        product = get_object_or_404(Products, id=id)

        if quantity > product.stock:
            messages.error(request, 'Não temos essa quantidade em estoque!')
            return redirect('home:add_to_cart', id)

        else:
            product.stock -= quantity
            product.save()

        cart_item, _ = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': 0}
        )

        cart_item.add_quatity(quantity)

    return redirect('home:index')

    # else:
    #     raise Http404()


def remove_from_cart(request, id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity-to-remove', 1))

        cart, _ = Cart.objects.get_or_create(user=request.user)

        product = get_object_or_404(Products, id=id)

        cart_item, _ = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
        )

        cart_item.quantity -= quantity
        cart_item.save()

    return redirect('home:cart_detail')


def cart_detail_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)

    cart_item = CartItem.objects.filter(
        cart=cart,
    )

    products = cart_item.all()

    total_price = 0

    for product in products:
        if product.quantity <= 0:
            product.delete()
            return redirect('home:cart_detail')

        total_price += product.product.price

    return render(request, 'home/pages/cart_detail.html', context={
        'products': products,
        'total_price': total_price
    })

# No comprar produtos a hora que
# a pessoa for digitar o cep
# se for diferentes da que eu
# colocar permitido dar um erro
