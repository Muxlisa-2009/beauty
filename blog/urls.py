from django.urls import path
from .views import *


urlpatterns = [
    path('',index,name='index'),
    path('cart', cart, name='cart'),
    path( 'shop/', shop, name='shop'),
    path('women/', women, name='women'),
    path('not_found/', not_found, name='not_found'),
    path('checkout/', checkout, name='checkout'),
]