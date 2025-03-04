from django.shortcuts import render
from .models import Meal

def menu(request):
    meals = Meal.objects.all()  # Fetch all menu items from the database
    return render(request, 'orders/menu.html', {'meals': meals})
