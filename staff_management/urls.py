from django.urls import path
from staff_management import views

app_name = 'staff'

urlpatterns = [
    path('', views.HomeListView.as_view(), name='index'),
    path('add_product/', views.AddProductView.as_view(), name='add_product'),
    path('edit_product/<id>/',
         views.EditProductView.as_view(),
         name='edit_product'
         ),
    path('delete_product/<id>/',
         views.DeleteProductView.as_view(),
         name='delete_product'
         ),
]
