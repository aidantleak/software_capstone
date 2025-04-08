from django.urls import path, include
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.home, name='root'),
    path('home/', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('cart/', views.view_cart, name='view_cart'),
    path('add-to-cart/<int:meal_id>/', views.add_to_cart, name='add_to_cart'),
    path('place-order/', views.place_order, name='place_order'),
    path('order-placed/<int:order_id>/', views.order_placed, name='order_placed'),
    
    # Orders
    path('order-history/', views.order_history, name='order_history'),
    path('order-details/<int:order_id>/', views.order_details, name='order_details'),
    path('toggle-favorite-order/<int:order_id>/', views.toggle_favorite_order, name='toggle_favorite_order'),
    path('reorder/<int:order_id>/', views.reorder_order, name='reorder_order'),
    path('check-status/<int:order_id>/', views.check_order_status, name='check_order_status'),

    # Auth
    path('register/', views.register, name='register'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),

    # Account Pages
    path('account/', views.account, name='account'),
    path('edit-account/', views.edit_account, name='edit_account'),
    
    # Cart Count
    path('get-cart-count/', views.get_cart_count, name='get_cart_count'),

    # Triton Service
    path('triton-service/', views.triton_service, name='triton_service'),
    path('update-order-status/<int:order_id>/', views.update_order_status, name='update_order_status'),
]
