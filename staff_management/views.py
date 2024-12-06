from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth.decorators import user_passes_test
from staff_management.forms import AddProduct
from home.models import Products


def is_staff(user):
    return user.is_staff


@user_passes_test(is_staff, login_url='authors:login')
def home(request):
    if not request.user.has_perm('app_name.change_item'):
        raise Http404()

    products = Products.objects.all()

    return render(request, 'global/pages/base_page.html', context={
        'title': 'Staff',
        'products': products,
        'is_staff': True
    })


@user_passes_test(is_staff, login_url='authors:login')
def add_product(request):
    if request.method == 'POST':
        form = AddProduct(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user

            product.save()

            cover = form.cleaned_data['cover']

            product.cover = cover

            return redirect('staff:index')

    else:
        form = AddProduct()

    return render(request, 'staff_management/pages/crud_item.html', context={
        'form': form
    })
