from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView

from home.models import Ordered

from .index import DeleteViewMixin, UserPassesTestMixin


class OrderedIndexView(UserPassesTestMixin, ListView):
    template_name = 'staff_management/pages/ordered.html'
    context_object_name = 'ordereds'
    model = Ordered
    paginate_by = 10
    paginator_class = Paginator
    ordering = ['id']

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context.update({
            'title': 'Pedidos',
            'is_staff': True,
            'search_url': reverse('staff:staff_ordered_search')
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


class StaffOrderedSearchListView(ListView):
    template_name = 'staff_management/pages/search_ordereds.html'
    context_object_name = 'ordereds'
    model = Ordered
    paginator_class = Paginator
    paginate_by = 10
    ordering = ['id']

    def get_queryset(self, *args, **kwargs):
        search_term = self.request.GET.get('q', '')

        if not search_term:
            raise Http404()

        queryset = super().get_queryset(*args, **kwargs)

        queryset = queryset.filter(
            Q(
                Q(number_ordered__icontains=search_term) |
                Q(first_name__icontains=search_term) |
                Q(last_name__icontains=search_term)
            )
        )

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get('q', '').strip()

        context.update({
            'page_title': f'Search for "{search_term}" |',
            'search_term': search_term,
            'additional_url_query': f'&q={search_term}',
            'is_staff': True,
        })

        return context
