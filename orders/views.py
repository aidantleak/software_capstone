from django.shortcuts import render
from .models import Meal

def menu(request):
    meals = Meal.objects.all()  # Fetch all menu items from the database
    return render(request, 'orders/menu.html', {'meals': meals})


# for each html page we need to create a view and a url
def home(request):
    return render(request, 'orders/home.html', {'home': home})
