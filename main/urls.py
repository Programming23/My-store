

from django.urls import path, include, re_path
from . import views, command
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    
    path('', views.index, name="index"),
    path('cart/', command.cartPage, name="cart"),
    path('checkout/', command.checkout, name="checkout"),
    path('order/<str:order_num>/', command.end_order, name="end_order"),
    path('contact-us/', views.contact_us, name="contact"),
    path('remove_item/<int:item>/', command.removeItemCart, name="remove_cart_item"),
    path('product/<str:name>/', views.productPage, name="product"),
]

