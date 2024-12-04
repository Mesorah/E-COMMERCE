from django.shortcuts import render
from django.contrib.auth.views import LoginView


class AuthorLoginView(LoginView):
    template_name = "authors/pages/base_page.html"
    redirect_authenticated_user = False


def test(request):
    return render(request, 'global/pages/base_page.html')
