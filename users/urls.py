from django.urls import path
from . import views

urlpatterns = [
    path('profile',views.profile,name='profile'),
    path('editprofile',views.editprofile,name='editprofile'),
    path('add_to_cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('clients/', views.clients_view, name='clients'),
    path('footer/', views.footer_view, name='footer'),
]