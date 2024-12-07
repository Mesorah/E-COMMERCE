from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth.decorators import user_passes_test
from staff_management.forms import CrudProduct
from home.models import Products
from django.urls import reverse


def is_staff(user):
    return user.is_staff


@user_passes_test(is_staff, login_url='authors:login')
def home(request):
    products = Products.objects.all()

    return render(request, 'global/pages/base_page.html', context={
        'title': 'Staff',
        'products': products,
        'is_staff': True
    })


@user_passes_test(is_staff, login_url='authors:login')
def add_product(request):
    if request.method == 'POST':
        form = CrudProduct(request.POST, request.FILES)

        if form.is_valid():

            product = form.save(commit=False)
            product.user = request.user

            product.save()

            cover = form.cleaned_data['cover']

            product.cover = cover

            return redirect('staff:index')

    else:
        form = CrudProduct()

    return render(request, 'staff_management/pages/crud_item.html', context={
        'form': form,
        'form_url': reverse('staff:add_product'),
        'is_staff': True
    })


@user_passes_test(is_staff, login_url='authors:login')
def edit_product(request, id):
    product = Products.objects.filter(
            user=request.user,
            id=id
        ).first()

    if not product:
        raise Http404()

    if request.method == 'POST':
        form = CrudProduct(request.POST, request.FILES, instance=product)

        if form.is_valid():
            form.save()

            return redirect('staff:index')

    else:
        form = CrudProduct(instance=product)

    return render(request, 'staff_management/pages/crud_item.html', context={
        'form': form,
        'form_url': reverse('staff:edit_product', args=[id]),
        'is_staff': True
    })


@user_passes_test(is_staff, login_url='authors:login')
def delete_product(request, id):
    # depois criar uma confirmação

    if request.method == 'POST':
        product = Products.objects.filter(
                user=request.user,
                id=id
            ).first()

        if not product:
            raise Http404()

        product.delete()

        return redirect('staff:index')

    else:
        raise Http404()
