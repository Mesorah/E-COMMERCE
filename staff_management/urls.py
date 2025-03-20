from django.urls import path

from staff_management import views

app_name = 'staff'

urlpatterns = [
     path('', views.HomeListView.as_view(), name='index'),

     path('product/create/',
          views.ProductCreateView.as_view(),
          name='add_product'
          ),
     path('product/update/<slug:slug>/',
          views.ProductUpdateView.as_view(),
          name='update_product'
          ),
     path('product/delete/<int:pk>/',
          views.ProductDeleteView.as_view(),
          name='delete_product'
          ),
     path('products/search/',
          views.StaffSearchListView.as_view(),
          name="staff_search"
          ),

     path('ordered/index/',
          views.OrderedIndexView.as_view(),
          name='ordered_index'
          ),
     path('ordered/detail/<int:pk>/',
          views.OrderedDetailView.as_view(),
          name='ordered_detail'
          ),

     path('ordered/complete/',
          views.CompleteOrderedView.as_view(),
          name='ordered_complete'
          ),

     path('ordered/complete/<int:pk>/',
          views.OrderedCompleteView.as_view(),
          name='complete_ordered'
          ),

     path('ordereds/search/',
          views.StaffOrderedSearchListView.as_view(),
          name="staff_ordered_search"
          ),

     path('clients/',
          views.ClientsListView.as_view(),
          name='clients'
          ),
     path('client/<int:pk>/',
          views.ClientListOrderedDetailView.as_view(),
          name='client_list_ordered'
          ),
     path('clients/search/',
          views.StaffClientsSearchListView.as_view(),
          name="staff_client_search"
          ),

     path('support/',
          views.SupportStaff.as_view(),
          name='support_staff'
          ),
     path('support/view/',
          views.SupportViewStaff.as_view(),
          name='support_view_staff'
          ),
     path('support/question/delete/<int:pk>/',
          views.SupportQuestionDelete.as_view(),
          name='support_question_delete'
          ),
     path('support/question/detail/<int:pk>/',
          views.SupportQuestionDetail.as_view(),
          name='support_question_detail'
          ),
]
