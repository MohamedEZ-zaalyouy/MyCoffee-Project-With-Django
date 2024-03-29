
from django.urls import path
from . import views


urlpatterns = [
    path('add_to_cart',views.add_to_cart, name='add_to_cart'),
    path('cart',views.cart, name='cart'),
    path('remove_from_cart/<int:orderdetails_id>',views.remove_from_cart, name='remove_from_cart'),
    path('add_QTY/<int:orderdetails_id>',views.add_QTY, name='add_QTY'),
    path('sub_QTY/<int:orderdetails_id>',views.sub_QTY, name='sub_QTY'),
    path('payment',views.payment, name='payment'),
    path('orders',views.show_orders, name='orders'),
    ]
