from django.urls import path
from home import views

app_name = 'home'

urlpatterns = [
    path('', views.home, name='index'),
    path('product/<id>/', views.view_page, name='view_page'),
]
