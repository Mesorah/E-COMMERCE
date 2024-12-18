import os

from django.contrib.auth.decorators import user_passes_test
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from home.models import CustomerQuestion
from staff_management.forms import SupportStaffForm

from .index import is_staff


@user_passes_test(is_staff, login_url='authors:login')
def support_staff(request):
    if request.method == 'POST':
        form = SupportStaffForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email', 'E-mail not found')
            answer = form.cleaned_data.get('answer', 'Answer not found')

            if email != 'E-mail not found' and answer != 'Answer not found':
                send_mail(
                    'Sobre sua dúvida',
                    answer,
                    os.environ.get('EMAIL_HOST_USER', 'email'),  # Remetente
                    [email],  # Destinatário
                    fail_silently=False,
                )

                return redirect('staff:index')
    else:
        form = SupportStaffForm()

    return render(
        request,
        'staff_management/pages/support_staff.html',
        context={
            'title': 'Suporte staff',
            'form': form
        }
    )


@user_passes_test(is_staff, login_url='authors:login')
def support_view_staff(request):
    questions = CustomerQuestion.objects.all()

    return render(
        request,
        'staff_management/pages/support_view_staff.html',
        context={
            'questions': questions
        }
    )


@user_passes_test(is_staff, login_url='authors:login')
def support_question_delete(request, id):
    if request.method == 'POST':
        question = CustomerQuestion.objects.filter(id=id)

        question.delete()

        return redirect('staff:support_view_staff')

    return redirect('staff:support_view_staff')


@user_passes_test(is_staff, login_url='authors:login')
def support_question_detail(request, id):
    question = CustomerQuestion.objects.filter(id=id).first()

    return render(
        request,
        'staff_management/pages/support_question_detail.html',
        context={
            'question': question
        }
    )


# Fazer um botão com que
# quando apertado ele
# vai na página de enviar
# o email ja com o email
# colocado
