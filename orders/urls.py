from django.urls import path
from .views import *
from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from .views import register, login_view
from django.contrib.auth.views import LogoutView
from orders import views

urlpatterns = [
    path('', home, name='root'),
    path('menu/', menu, name='menu'),
    path('home/', home, name='home'),
    path('place-order/', place_order, name='place_order'),
    path('add-to-cart/<int:meal_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),
    path('order-placed/<int:order_id>/', views.order_placed, name='order_placed'),
    path('accounts/', include('django.contrib.auth.urls')), 
    path('register/', register, name='register'),
    #path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('order-history/', order_history, name='order_history'),
    path('check-status/<int:order_id>/', views.check_order_status, name='check_order_status'),
 

    
]
