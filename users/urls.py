from django.urls import path
from . import views
# app_name = 'users'
urlpatterns = [
    path("", views.home, name="home"),

    path("register/", views.register, name="register"),
    path("login/", views.Login, name="login"),
    path("logout/", views.Logout, name="logout"),

    path("change_password/", views.change_password, name="change_password"),

    path("loggedin_contact/", views.loggedin_contact, name="loggedin_contact"),

    path("contact/", views.contact, name="contact"),
    
    path("product_view/<int:myid>/", views.product_view, name="product_view"),
    path("update_item/", views.updateItem, name="update_item"),
    path("place_bid/<int:myid>/", views.place_bid, name="place_bid"),

    path("cart/", views.cart, name="cart"),
    path("search/", views.search, name="search"),
    path("checkout/", views.checkout, name="checkout"),
    path('footer/', views.footer_view, name='footer'),
]