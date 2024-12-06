from django.urls import path
from staff_management import views

app_name = 'staff'

urlpatterns = [
    path('', views.home, name='index'),
    path('add_product/', views.add_product, name='add_product'),
    path('edit_product/<id>/', views.edit_product, name='edit_product'),
    path('delete_product/<id>/', views.delete_product, name='delete_product'),
]
