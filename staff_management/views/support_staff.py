import os

from django.contrib.auth.decorators import user_passes_test
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from .index import is_staff


@user_passes_test(is_staff, login_url='authors:login')
def support_staff(request):
    if request.method == 'POST':
        email = str(request.POST.get('email', 'E-mail not found'))
        answer = str(request.POST.get('answer', 'Answer not found'))

    if email != 'E-mail not found' or answer != 'Answer not found':
        send_mail(
            'Sobre sua dúvida',
            answer,
            os.environ.get('EMAIL_HOST_USER', 'email'),  # Remetente
            [email],  # Destinatário
            fail_silently=False,
        )

        return redirect('staff:index')

    return render(
        request,
        'staff_management/pages/support_staff.html',
        context={
            'title': 'Suporte staff'
        }
    )
