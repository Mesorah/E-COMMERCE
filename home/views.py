from django.shortcuts import render
from home.models import Products


def home(request):
    products = Products.objects.all()

    return render(request, 'global/pages/base_page.html', context={
        'products': products
    })
