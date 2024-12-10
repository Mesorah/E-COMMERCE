from django.shortcuts import redirect, render

from home.forms import PaymentForm


def payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)

        if form.is_valid():
            return redirect('home:index')

    else:
        form = PaymentForm()

    return render(request, 'home/pages/payment.html', context={
        'form': form
    })
