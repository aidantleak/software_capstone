from django.urls import path
from .views import menu  # Ensure views are correctly imported

urlpatterns = [
    path('menu/', menu, name ='menu'),
]
