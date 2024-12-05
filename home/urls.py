from django.urls import path
from home import views

app_name = 'home'

urlpatterns = [
    path('', views.HomeListView.as_view(), name='index'),
    path('product/<pk>/', views.ViewPageDetailView.as_view(), name='view_page'),
]
