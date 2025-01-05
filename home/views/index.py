from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.urls import reverse
from django.views.generic import DetailView, ListView

from home.models import CartItem, Products


class HomeListView(ListView):
    template_name = 'global/pages/base_page.html'
    model = Products
    context_object_name = 'products'
    paginate_by = 10
    paginator_class = Paginator
    ordering = ['-id']

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
            'search_url': reverse('home:home_search'),
            'name': 'product'
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

        product = self.object

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


class BaseSearchListView(ListView):
    template_name = 'global/pages/search_product.html'
    model = Products
    paginate_by = 10
    paginator_class = Paginator
    context_object_name = 'products'
    ordering = ['-id']
    is_published = True

    def get_queryset(self, *args, **kwargs):
        search_term = self.request.GET.get('q', '')

        if not search_term:
            raise Http404()

        queryset = super().get_queryset(*args, **kwargs)

        queryset = queryset.filter(
            Q(
                Q(name__icontains=search_term)
            )
        )

        if self.is_published:
            queryset = queryset.filter(is_published=True)

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get('q', '').strip()

        context.update({
            'title': f'Search for "{search_term}" |',
            'search_term': search_term,
            'additional_url_query': f'&q={search_term}',
        })

        return context


class HomeSearchListView(BaseSearchListView):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context.update({
            'name': 'product'
        })

        return context
