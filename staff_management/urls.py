from django.urls import path
from staff_management import views

app_name = 'staff'

urlpatterns = [
    path('', views.home, name='index'),
    path('add_product/', views.add_product, name='add_product')
]
