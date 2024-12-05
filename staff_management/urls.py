from django.urls import path
from staff_management import views

app_name = 'staff'

urlpatterns = [
    path('', views.testing, name='register'),
]
