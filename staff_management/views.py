from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from staff_management.forms import CrudProduct
from django.views.generic import ListView
from home.models import Products
from django.http import Http404
from django.urls import reverse
from django.views import View


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


class AddProductView(UserPassesTestMixin, View):
    def get_render(self, form):
        return render(self.request,
                      'staff_management/pages/crud_item.html',
                      context={'form': form,
                               'form_url': reverse('staff:add_product'),
                               'is_staff': True
                               })

    def get(self, request):
        form = CrudProduct()

        return self.get_render(form)

    def post(self, request):
        form = CrudProduct(self.request.POST, self.request.FILES)

        if form.is_valid():

            product = form.save(commit=False)
            product.user = self.request.user

            product.save()

            cover = form.cleaned_data['cover']

            product.cover = cover

            return redirect('staff:index')

        return self.get_render(form)


class EditProductView(UserPassesTestMixin, View):
    def get_render(self, form, id):
        return render(
            self.request,
            'staff_management/pages/crud_item.html',
            context={
                'form': form,
                'form_url': reverse('staff:edit_product',
                                    args=[id]), 'is_staff': True})

    def get_product(self, id):
        product = Products.objects.filter(
            user=self.request.user,
            id=id
        ).first()

        if not product:
            raise Http404()

        return product

    def get(self, request, id):
        product = self.get_product(id)

        form = CrudProduct(instance=product)

        return self.get_render(form, id)

    def post(self, request, id):
        product = self.get_product(id)

        form = CrudProduct(self.request.POST, self.request.FILES,
                           instance=product
                           )

        if form.is_valid():
            form.save()

            return redirect('staff:index')

        return self.get_render(form, id)


class DeleteProductView(UserPassesTestMixin, View):
    # depois criar uma confirmação
    def post(self, request, id):
        product = Products.objects.filter(
                user=self.request.user,
                id=id
            ).first()

        if not product:
            raise Http404()

        product.delete()

        return redirect('staff:index')
