from home.models import Products, Cart
from django.http import Http404
from django.views.generic import ListView, DetailView
from django.shortcuts import redirect


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
            'title': 'Home'
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

        cart = Cart.objects.filter(
            products=self.kwargs.get('pk'),
            pk=self.kwargs.get('pk')
        ).first()

        context.update({
            'title': 'View Page',
            'stock': product.stock,
            'have_produtct': cart
        })

        return context


def add_to_cart(request, id):
    # adicionar a quantidade
    cart = Cart.objects.filter(
        user=request.user
    ).first()

    if not cart:
        cart = Cart.objects.create(
            user=request.user
        )

    cart.products.add(id)

    return redirect('home:index')


def remove_from_cart(request, id):
    cart = Cart.objects.filter(
        user=request.user
    ).first()

    if not cart:
        return redirect('home:index')

    cart.products.remove(id)

    return redirect('home:index')



# No comprar produtos a hora que
# a pessoa for digitar o cep
# se for diferentes da que eu
# colocar permitido dar um erro
