from django.shortcuts import render
from .models import Meal
from django.contrib.auth import logout
def menu(request):
    meals = Meal.objects.all()  # Fetch all menu items from the database
    return render(request, 'orders/menu.html', {'meals': meals})

def home(request):
    return render(request, "home.html")

def logout_view(request):
    logout(request)
    return redirect("/")
