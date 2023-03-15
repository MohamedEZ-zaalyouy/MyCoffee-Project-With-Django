
from django.urls import path
from . import views


urlpatterns = [
    path('add_to_cart',views.add_to_cart, name='add_to_cart'),
    path('cart',views.cart, name='cart'),
    path('remove_from_cart/<int:orderdetails_id>',views.remove_from_cart, name='remove_from_cart'),
    ]
