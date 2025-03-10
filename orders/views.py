from django.shortcuts import render, redirect
from .models import *


def menu(request):
    meals = Meal.objects.all()  # Get menu items from database
    return render(request, 'orders/menu.html', {'meals': meals})


# for each html page we need to create a view and a url
def home(request):
    return render(request, 'orders/home.html', {'home': home})


def place_order(request):
    cart = request.session.get('cart', [])
    if not cart:
        return redirect('menu')  # Redirect if cart is empty
    order = Order.objects.create(user=request.user if request.user.is_authenticated else None)
    for item in cart:
        meal = Meal.objects.get(id=item['meal_id'])
        OrderItem.objects.create(
            order=order,
            meal=meal,
            quantity=item['quantity'],
            price_at_order=item['price']
        )

    request.session['cart'] = []  # Clear the cart after order is placed
    return redirect('order_placed')  # Redirect to a success page


def add_to_cart(request, meal_id):
    meal = Meal.objects.get(id=meal_id)
    side = request.POST.get('side')
    quantity = int(request.POST.get('quantity', 1))

    cart = request.session.get('cart', [])  # Get cart from session (or create a new one)

    # Add meal details to the cart
    cart.append({
        'meal_id': meal.id,
        'name': meal.name,
        'price': float(meal.price),  # Convert Decimal to float for session storage
        'side': side,
        'quantity': quantity,
        'image': meal.image.url if meal.image else None,
    })

    request.session['cart'] = cart  # Save cart back to session
    return redirect('menu')  # Redirect back to menu


def view_cart(request):
    cart = request.session.get('cart', [])  # Retrieve cart items from session
    return render(request, 'orders/cart.html', {'cart': cart})

def order_placed(request):
    return render(request, 'orders/order_placed.html')
