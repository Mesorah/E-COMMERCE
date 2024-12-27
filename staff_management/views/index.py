from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from django.http import Http404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from home.models import Products
from home.views.index import BaseSearchListView
from staff_management.forms import CrudProduct


def is_staff(user):
    return user.is_staff


class UserPassesTestMixin:
    @method_decorator(user_passes_test(is_staff, login_url='authors:login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class HomeListView(UserPassesTestMixin, ListView):
    model = Products
    template_name = 'global/pages/base_page.html'
    context_object_name = 'products'
    paginate_by = 10
    paginator_class = Paginator
    ordering = ['-id']

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context.update({
            'title': 'Staff',
            'is_staff': True,
            'search_url': reverse('staff:staff_search'),
            'name': 'product'
        })

        return context


class ProductCreateView(UserPassesTestMixin, CreateView):
    template_name = 'staff_management/pages/crud_item.html'
    form_class = CrudProduct
    success_url = reverse_lazy('staff:index')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context.update({
            'title': 'Adicionar Produto',
            'form_url': reverse('staff:add_product'),
            'is_staff': True
        })

        return context

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super().form_valid(form)


class ProductUpdateView(UserPassesTestMixin, UpdateView):
    template_name = 'staff_management/pages/crud_item.html'
    model = Products
    form_class = CrudProduct
    success_url = reverse_lazy('staff:index')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context.update({
            'title': 'Editar Produto',
            'form_url': reverse('staff:update_product',
                                args=[self.kwargs['pk']]),
            'is_staff': True
        })

        return context


class DeleteViewMixin(UserPassesTestMixin, DeleteView):
    model = Products
    success_url = reverse_lazy('staff:index')

    def get(self, *args, **kwargs):
        raise Http404()


class ProductDeleteView(DeleteViewMixin):
    pass


class StaffSearchListView(BaseSearchListView):
    is_published = False

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context.update({
            'is_staff': True,
            'name': 'product'
        })

        return context
