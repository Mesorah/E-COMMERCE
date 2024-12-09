from django.urls import path
from home import views

app_name = 'home'

urlpatterns = [
    path('', views.HomeListView.as_view(), name='index'),
    path('product/<pk>/',
         views.PageDetailView.as_view(),
         name='view_page'
         ),
    path('add_to_cart/<id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_to_cart/<id>/',
         views.remove_from_cart,
         name='remove_from_cart'
         ),
    path('cart_detail/',
         views.cart_detail_view,
         name='cart_detail'
         ),
]
