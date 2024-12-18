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
          views.OrderedIndexView.as_view(),
          name='ordered_index'
          ),
     path('ordered_detail/<pk>/',
          views.OrderedDetailView.as_view(),
          name='ordered_detail'
          ),
     path('delete_ordered/<pk>/',
          views.OrderedDeleteView.as_view(),
          name='delete_ordered'
          ),

     path('clients/',
          views.ClientsListView.as_view(),
          name='clients'
          ),
     path('client/<pk>/',
          views.ClientListOrderedDetailView.as_view(),
          name='client_list_ordered'
          ),

     path('support_staff/',
          views.support_staff,
          name='support_staff'
          ),
     path('support_view_staff/',
          views.support_view_staff,
          name='support_view_staff'
          ),
     path('support_delete_question/<id>/',
          views.support_delete_question,
          name='support_delete_question'
          ),
     path('support_question_detail/<id>/',
          views.support_question_detail,
          name='support_question_detail'
          ),
]
