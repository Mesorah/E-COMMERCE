from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
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
    login_url = reverse_lazy('authors:login')
    template_name = 'home/pages/support_completed.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context.update({
            'title': 'Pergunta enviada'
        })

        return context


class SupportClient(LoginRequiredMixin, View):
    login_url = reverse_lazy('authors:login')

    def get_render(self):
        return render(self.request, 'home/pages/support.html', context={
            'title': 'Suporte'
        })

    def get_customer_question(self):
        question = str(
            self.request.POST.get('question', 'Resposta não enviada')
        )

        customer_question = CustomerQuestion(
            user=self.request.user,
            question=question
        )

        return customer_question

    def get(self, request):
        return self.get_render()

    def post(self, request):
        customer_question = self.get_customer_question()

        customer_question.save()

        return redirect('home:support_completed')
