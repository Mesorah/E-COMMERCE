from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from home.models import CustomerQuestion


def faq(request):
    return render(request, 'home/pages/faq.html', context={
        'title': 'FAQ - Perguntas Frequentes'
    })


def support_completed(request):
    return render(request, 'home/pages/support_completed.html', context={
        'title': 'Pergunta enviada'
    })


@login_required(login_url='authors:login')
def support_client(request):
    if request.method == 'POST':
        question = str(request.POST.get('question', 'Resposta não enviada'))

        customer_question = CustomerQuestion(
            user=request.user,
            question=question
        )

        customer_question.save()

        return redirect('home:support_completed')

    return render(request, 'home/pages/support.html', context={
        'title': 'Suporte'
    })
