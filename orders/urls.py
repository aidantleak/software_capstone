from django.urls import path
from .views import menu  # Ensure views are correctly imported

urlpatterns = [
    path('menu/', menu, name ='menu'),
]
urlpatterns = [
    path("", views.home),
    path("logout", views.logout_view),
]
