from django.urls import path
from .views import *


urlpatterns = [
    path('',index,name='index'),
    path('cart', cart, name='cart'),
    path( 'shop/', shop, name='shop'),
    path('women/', women, name='women'),
    path('not_found/', not_found, name='not_found'),
    path('checkout/', checkout, name='checkout'),
    path('shop/', shop, name='shop'),
    path('product/<slug:slug>/', product_detail, name='product_detail'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_detail, name='cart_detail'),
]