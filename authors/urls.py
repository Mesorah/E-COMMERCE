from django.urls import path
from authors import views

app_name = 'authors'

urlpatterns = [
    path('', views.home, name='index'),
]
