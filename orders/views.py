from django.shortcuts import render, redirect
from .models import Meal, Order, OrderItem
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

def menu(request):
    meals = Meal.objects.all()
    return render(request, 'orders/menu.html', {'meals': meals})

def home(request):
    return render(request, 'orders/home.html')

@login_required
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
    return redirect('order_placed', order_id=order.id)


    # Send email to admin
    admin_email = settings.ADMIN_EMAIL 
    send_mail(
        'New Order Placed',
        f'An order has been placed with the following items:\n\n{order_items}',
        settings.DEFAULT_FROM_EMAIL,
        [admin_email],
        fail_silently=False,
    )
    # Send email to the user
    if request.user.is_authenticated:
        user_email = request.user.email
        send_mail(
            'Order Confirmation',
            f'Thank you for your order! Here are the details:\n\n{order_items}',
            settings.DEFAULT_FROM_EMAIL,
            [user_email],
            fail_silently=False,
        )

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


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('place_order')  # Redirect to the order page
    else:
        form = CustomUserCreationForm()
    return render(request, 'orders/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            print("Logged in as:", user.username)
            return redirect('menu')  # Redirect to last visited page after login

    else:

        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})



@login_required
def order_history(request):
    all_orders = Order.objects.filter(user=request.user, status='completed').order_by('-created_at')
    favorite_orders = all_orders.filter(favorite=True)

    context = {
        'all_orders': all_orders,
        'favorite_orders': favorite_orders,
    }
    return render(request, 'orders/order_history.html', context)

def check_order_status(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        return JsonResponse({'status': order.status})
    except Order.DoesNotExist:
        return JsonResponse({'status': 'error'}, status=404)

def order_placed(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'orders/order_placed.html', {'order': order})

@login_required
def order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    items = OrderItem.objects.filter(order=order)
    return render(request, 'orders/order_details.html', {
        'order': order,
        'items': items,
    })

@login_required
def toggle_favorite_order(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)
    order.favorite = not order.favorite
    order.save()
    return redirect('order_details', order_id=order_id)

from django.contrib.auth.decorators import login_required

@login_required
def reorder_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        return redirect('order_history')  # fallback if someone tries to reorder someone else’s order

    cart = []

    for item in order.orderitem_set.all():
        cart.append({
            'meal_id': item.meal.id,
            'name': item.meal.name,
            'price': float(item.meal.price),  # Use current price
            'side': item.meal.side,
            'quantity': item.quantity,
            'image': item.meal.image.url if item.meal.image else None,
        })

    request.session['cart'] = cart
    return redirect('view_cart')
