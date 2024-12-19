from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from home.models import CustomerQuestion


class Faq(TemplateView):
    template_name = 'home/pages/faq.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context.update({
            'title': 'FAQ - Perguntas Frequentes'
        })

        return context


class SupportCompleted(LoginRequiredMixin, TemplateView):
    template_name = 'home/pages/support_completed.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context.update({
            'title': 'Pergunta enviada'
        })

        return context


@login_required(login_url='authors:login')
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
