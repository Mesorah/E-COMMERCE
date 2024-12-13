from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.urls import reverse_lazy

from home.models import Ordered

from .index import DeleteViewMixin, is_staff


@user_passes_test(is_staff, login_url='authors:login')
def ordered_index(request):
    ordereds = Ordered.objects.all()

    return render(request, 'staff_management/pages/ordered.html', context={
        'title': 'Pedidos',
        'ordereds': ordereds,
        'is_staff': True,
    })


class OrderedDeleteView(DeleteViewMixin):
    success_url = reverse_lazy('staff:ordered_index')
    model = Ordered


@user_passes_test(is_staff, login_url='authors:login')
def ordered_detail(request, id):
    order = Ordered.objects.filter(id=id).first()
    products = order.products.all()

    total_price = 0
    for product in products:
        total_price += product.product.price * product.quantity

    return render(request,
                  'staff_management/pages/ordered_detail.html',
                  context={
                      'title': 'Detalhe do pedido',
                      'order': order,
                      'is_staff': True,
                      'products': products,
                      'total_price': total_price
                    })

# Fazer página de cada cliente, com cada produto comprado
