from django.urls import path

from staff_management import views

app_name = 'staff'

urlpatterns = [
     path('', views.HomeListView.as_view(), name='index'),
     path('add_product/',
          views.ProductCreateView.as_view(),
          name='add_product'
          ),
     path('update_product/<pk>/',
          views.ProductUpdateView.as_view(),
          name='update_product'
          ),
     path('delete_product/<pk>/',
          views.ProductDeleteView.as_view(),
          name='delete_product'
          ),

     path('ordered_index/',
          views.ordered_index,
          name='ordered_index'
          ),
     path('ordered_detail/<id>/',
          views.ordered_detail,
          name='ordered_detail'
          ),
     path('delete_ordered/<pk>/',
          views.OrderedDeleteView.as_view(),
          name='delete_ordered'
          ),
]
