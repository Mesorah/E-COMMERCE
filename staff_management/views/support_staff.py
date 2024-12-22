import os

from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView

from home.models import CustomerQuestion
from staff_management.forms import SupportStaffForm

from .index import DeleteViewMixin, UserPassesTestMixin


class SupportStaff(UserPassesTestMixin, View):
    def get_data(self):
        email = self.request.POST.get('email')

        data = {
            'email': email,
        }

        return data

    def get_render(self, form, data):
        return render(
            self.request,
            'staff_management/pages/support_staff.html',
            context={
                'title': 'Suporte staff',
                'form': form,
                'initial_data': data,
            }
        )

    def send_email(self, answer, email):
        email = send_mail(
                'Sobre sua dúvida',
                answer,
                os.environ.get('EMAIL_HOST_USER', 'email'),  # Remetente
                [email],  # Destinatário
                fail_silently=False,
            )

        return email

    def get(self, request):
        data = self.get_data()

        form = SupportStaffForm(initial=data)

        return self.get_render(form, data)

    def post(self, request):
        form = SupportStaffForm(self.request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email')
            answer = form.cleaned_data.get('answer')

            self.send_email(answer, email)

            return redirect('staff:support_view_staff')


# Talvez quando enviada a resposta 'delete' a dúvida
class SupportViewStaff(UserPassesTestMixin, ListView):
    template_name = 'staff_management/pages/support_view_staff.html'
    model = CustomerQuestion
    context_object_name = 'questions'
    paginate_by = 10
    paginator_class = Paginator

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context.update({
            'title': 'Support staff'
        })

        return context


class SupportQuestionDelete(DeleteViewMixin):
    model = CustomerQuestion
    success_url = reverse_lazy('staff:support_view_staff')


class SupportQuestionDetail(UserPassesTestMixin, DetailView):
    template_name = 'staff_management/pages/support_question_detail.html'
    model = CustomerQuestion
    context_object_name = 'question'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context.update({
            'title': 'Detail question'
        })

        return context
