from django.urls import path

from home import views

app_name = 'home'

urlpatterns = [
     path('', views.HomeListView.as_view(), name='index'),
     path('product/<pk>/',
          views.PageDetailView.as_view(),
          name='view_page'
          ),

     path('add_to_cart/<id>/',
          views.AddToCartView.as_view(),
          name='add_to_cart'
          ),
     path('remove_to_cart/<id>/',
          views.RemoveFromCartView.as_view(),
          name='remove_from_cart'
          ),
     path('cart_detail/',
          views.CartDetailView.as_view(),
          name='cart_detail'
          ),

     path('payment/',
          views.payment,
          name='payment'
          ),
]
