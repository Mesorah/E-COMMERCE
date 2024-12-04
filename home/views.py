from django.shortcuts import render


def home(request):
    return render(request, 'global/pages/base_page.html')
