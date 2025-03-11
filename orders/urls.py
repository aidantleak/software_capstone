from django.urls import path
from .views import *

urlpatterns = [
    path('menu/', menu, name='menu'),
    path('home/', home, name='home'),
    path('place-order/', place_order, name='place_order'),
    path('add-to-cart/<int:meal_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),
    path('order-placed/', order_placed, name='order_placed'),
]
