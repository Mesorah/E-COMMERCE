from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView

from home.models import Ordered

from .index import DeleteViewMixin, UserPassesTestMixin


class OrderedIndexView(UserPassesTestMixin, ListView):
    template_name = 'staff_management/pages/ordered.html'
    context_object_name = 'ordereds'
    model = Ordered
    paginate_by = 10
    paginator_class = Paginator

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
