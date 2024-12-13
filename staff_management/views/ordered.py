from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView

from home.models import Cart, Ordered

from .index import DeleteViewMixin, UserPassesTestMixin


class OrderedIndexView(UserPassesTestMixin, ListView):
    template_name = 'staff_management/pages/ordered.html'
    context_object_name = 'ordereds'
    model = Ordered

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context.update({
            'title': 'Pedidos',
            'is_staff': True,
        })

        return context


class OrderedDeleteView(DeleteViewMixin):
    success_url = reverse_lazy('staff:ordered_index')
    model = Ordered


class OrderedDetailView(UserPassesTestMixin, DetailView):
    template_name = 'staff_management/pages/ordered_detail.html'
    model = Ordered
    context_object_name = 'order'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        order = self.get_object()
        products = order.products.all()

        total_price = 0
        for product in products:
            total_price += product.product.price * product.quantity

        context.update({
            'title': 'Detalhe do pedido',
            'is_staff': True,
            'products': products,
            'total_price': total_price
        })

        return context


def clients_list(request):
    clients = Cart.objects.all()

    return render(request, 'staff_management/pages/clients.html', context={
        'title': 'Clientes',
        'clients': clients,
        'is_staff': True,
    })


def client_list_ordered(request, id):
    cart = get_object_or_404(Cart, id=id)

    # Filtra os pedidos associados ao usuário deste carrinho
    ordereds = Ordered.objects.filter(products__cart=cart).distinct()

    return render(request, 'staff_management/pages/ordered.html', context={
        'title': 'Cliente',
        'ordereds': ordereds,
        'is_staff': True,
    })
