from django.shortcuts import render
from home.models import Products
from django.http import Http404


def home(request):
    products = Products.objects.all()

    return render(request, 'global/pages/base_page.html', context={
        'products': products
    })


def view_page(request, id):
    product = Products.objects.filter(id=id).first()

    if not product:
        raise Http404()

    return render(request, 'home/pages/view_page.html', context={
        'product': product
    })
