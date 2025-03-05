from django.urls import path

from home import views

app_name = 'home'

urlpatterns = [
     path('', views.HomeListView.as_view(), name='index'),
     path('product/<slug:slug>/',
          views.PageDetailView.as_view(),
          name='view_page'
          ),

     path('cart/add/<int:pk>/',
          views.AddToCartView.as_view(),
          name='add_to_cart'
          ),
     path('cart/remove/<int:pk>/',
          views.RemoveFromCartView.as_view(),
          name='remove_from_cart'
          ),
     path('cart/detail/',
          views.CartDetailView.as_view(),
          name='cart_detail'
          ),

     path('payment/',
          views.PaymentView.as_view(),
          name='payment'
          ),

     path('faq/',
          views.Faq.as_view(),
          name='faq',
          ),

     path('support/',
          views.SupportClient.as_view(),
          name='support_client',
          ),
     path('support/completed/',
          views.SupportCompleted.as_view(),
          name='support_completed',
          ),

     path('products/search/',
          views.HomeSearchListView.as_view(),
          name="home_search"
          ),
]
