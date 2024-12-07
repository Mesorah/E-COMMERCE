from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from staff_management.forms import CrudProduct
from django.urls import reverse, reverse_lazy
from home.models import Products
from django.http import Http404


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

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context.update({
            'title': 'Staff',
            'is_staff': True
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


class ProductDeleteView(UserPassesTestMixin, DeleteView):
    # depois criar uma confirmação
    model = Products
    success_url = reverse_lazy('staff:index')

    def get(self, *args, **kwargs):
        raise Http404()
