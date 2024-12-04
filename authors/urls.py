from django.urls import path
from authors import views

app_name = 'authors'

urlpatterns = [
    path('login/', views.AuthorLoginView.as_view(), name='login'),
    path('logout/', views.AuthorLogoutView.as_view(), name='logout'),
]
