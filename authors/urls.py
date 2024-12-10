from django.urls import path

from authors import views

app_name = 'authors'

urlpatterns = [
    path('change_password/',
         views.AuthorPasswordChangeView.as_view(),
         name='change_password'
         ),
    path('register/', views.AuthorRegisterView.as_view(), name='register'),
    path('login/', views.AuthorLoginView.as_view(), name='login'),
    path('logout/', views.AuthorLogoutView.as_view(), name='logout'),
]
