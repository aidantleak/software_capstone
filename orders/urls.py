from django.urls import path
from .views import *  

urlpatterns = [
    path('menu/', menu, name ='menu'),
    path('home/', home, name ='home'),
]
