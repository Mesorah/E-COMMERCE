from django.shortcuts import render


def page(request):
    return render(request, 'global/pages/base_page.html')
