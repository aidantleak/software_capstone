from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm

def menu(request):
    meals = Meal.objects.all()
    return render(request, 'orders/menu.html', {'meals': meals})

def home(request):
    return render(request, 'orders/home.html')

def place_order(request):
    cart = request.session.get('cart', [])
    if not cart:
        return redirect('menu')
    order = Order.objects.create(user=request.user if request.user.is_authenticated else None)
    for item in cart:
        meal = Meal.objects.get(id=item['meal_id'])
        OrderItem.objects.create(
            order=order,
            meal=meal,
            quantity=item['quantity'],
            price_at_order=item['price']
        )
    request.session['cart'] = []
    return redirect('order_placed')

def add_to_cart(request, meal_id):
    meal = Meal.objects.get(id=meal_id)
    side = request.POST.get('side')
    quantity = int(request.POST.get('quantity', 1))
    cart = request.session.get('cart', [])
    cart.append({
        'meal_id': meal.id,
        'name': meal.name,
        'price': float(meal.price),
        'side': side,
        'quantity': quantity,
        'image': meal.image.url if meal.image else None,
    })
    request.session['cart'] = cart
    return redirect('menu')

def view_cart(request):
    cart = request.session.get('cart', [])
    return render(request, 'orders/cart.html', {'cart': cart})

def order_placed(request):
    return render(request, 'orders/order_placed.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'orders/register.html', {'form': form})
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to a home page after login
    else:
        form = AuthenticationForm()
    return render(request, 'orders/login.html', {'form': form})