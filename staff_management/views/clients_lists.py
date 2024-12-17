from django.views.generic import ListView

from home.models import Cart, Ordered

from .index import UserPassesTestMixin


class ClientsListView(UserPassesTestMixin, ListView):
    template_name = 'staff_management/pages/clients.html'
    context_object_name = 'clients'
    model = Cart

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context.update({
            'title': 'Clientes',
            'is_staff': True,
        })

        return context


class ClientListOrderedDetailView(UserPassesTestMixin, ListView):
    template_name = 'staff_management/pages/ordered.html'
    context_object_name = 'ordereds'
    model = Ordered

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)

        cart = Cart.objects.filter(pk=self.kwargs.get('pk')).first()

        queryset = queryset.filter(
            products__cart=cart
        ).distinct()

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context.update({
            'title': 'Cliente',
            'is_staff': True,
        })

        return context
