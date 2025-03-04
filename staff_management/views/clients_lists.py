from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.urls import reverse
from django.views.generic import ListView

from authors.models import UserProfile
from home.models import Ordered

from .index import UserPassesTestMixin


class ClientsListView(UserPassesTestMixin, ListView):
    template_name = 'staff_management/pages/clients.html'
    context_object_name = 'clients'
    model = UserProfile
    paginate_by = 10
    paginator_class = Paginator
    ordering = ['-id']

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)

        queryset = queryset.select_related('user')

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context.update({
            'title': 'Clientes',
            'is_staff': True,
            'search_url': reverse('staff:staff_client_search'),
            'name': 'client'
        })

        return context


class ClientListOrderedDetailView(UserPassesTestMixin, ListView):
    # Uso o ListView, pois é um detalhe do cliente
    # só que pode ter vários pedidos
    template_name = 'staff_management/pages/ordered.html'
    context_object_name = 'ordereds'
    model = Ordered
    paginate_by = 10
    paginator_class = Paginator
    ordering = ['id']

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)

        user_profile = UserProfile.objects.filter(
            pk=self.kwargs.get('pk')
        ).first()

        user = user_profile.user

        # Pegando os users dos Cart_items e
        # do Cart_item pegando o User base
        queryset = queryset.filter(
            products__user__user=user
        ).all()

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context.update({
            'title': 'Cliente',
            'is_staff': True,
        })

        return context


class StaffClientsSearchListView(ListView):
    template_name = 'staff_management/pages/search_clients.html'
    context_object_name = 'clients'
    model = UserProfile
    paginator_class = Paginator
    paginate_by = 10
    ordering = ['-id']

    def get_queryset(self, *args, **kwargs):
        search_term = self.request.GET.get('q', '')

        if not search_term:
            raise Http404()

        queryset = super().get_queryset(*args, **kwargs)

        queryset = queryset.filter(
            Q(
                Q(id__icontains=search_term)
            )
        )

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get('q', '').strip()

        context.update({
            'title': f'Search for "{search_term}" |',
            'search_term': search_term,
            'additional_url_query': f'&q={search_term}',
            'is_staff': True,
            'name': 'client'
        })

        return context
