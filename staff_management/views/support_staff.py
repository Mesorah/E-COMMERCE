import os

from django.contrib.auth.decorators import user_passes_test
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from home.models import CustomerQuestion
from staff_management.forms import SupportStaffForm

from .index import is_staff


@user_passes_test(is_staff, login_url='authors:login')
def support_staff(request):
    email = request.POST.get('email')

    data = {
        'email': email,
    }

    if request.method == 'POST':
        form = SupportStaffForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email')
            answer = form.cleaned_data.get('answer')

            send_mail(
                'Sobre sua dúvida',
                answer,
                os.environ.get('EMAIL_HOST_USER', 'email'),  # Remetente
                [email],  # Destinatário
                fail_silently=False,
            )

            return redirect('staff:index')
    else:
        form = SupportStaffForm(initial=data)

    return render(
        request,
        'staff_management/pages/support_staff.html',
        context={
            'title': 'Suporte staff',
            'form': form,
            'initial_data': data,
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
