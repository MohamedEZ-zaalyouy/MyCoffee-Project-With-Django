from django.urls import path
from . import views

urlpatterns = [
    path('signin', views.signin , name='signin'),
    path('signup', views.signup , name='signup'),
    path('profile', views.profile , name='profile'),
    path('logout', views.LogOut , name='logout'),
    path('add_product_favorites/<int:pro_id>', views.add_product_favorites , name='add_product_favorites'),
    path('product_favorites', views.product_favorites , name='product_favorites'),
]
