from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from decimal import Decimal
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import PasswordResetForm

from .models import Meal, Order, OrderItem, UserProfile
from .forms import CustomUserCreationForm

def home(request):
    return render(request, 'orders/home.html')

@login_required
def view_cart(request):
    cart = request.session.get('cart', [])
    total = sum(item['price'] * item['quantity'] for item in cart)
    total_quantity = sum(item['quantity'] for item in cart)
    return render(request, 'orders/cart.html', {'cart': cart, 
                                                'total': total, 
                                                'total_quantity' : total_quantity})

def menu(request):
    meals = Meal.objects.all()
    return render(request, 'orders/menu.html', {'meals': meals})

@login_required
def add_to_cart(request, meal_id):
    meal = get_object_or_404(Meal, id=meal_id)
    side = request.POST.get('side')
    quantity = int(request.POST.get('quantity', 1))
    special_request = request.POST.get('special_request', '')

    cart = request.session.get('cart', [])
    cart.append({
        'meal_id': meal.id,
        'name': meal.name,
        'price': float(meal.price),
        'side': side,
        'quantity': quantity,
        'special_request': special_request,
        'image': meal.image.url if meal.image else None,
        'meal_swipe': meal.mealSwipe 
    })
    request.session['cart'] = cart
    messages.success(request, f'{meal.name} has been added to your cart!')
    return redirect('menu')

@login_required
def place_order(request):
    cart = request.session.get('cart', [])
    if not cart:
        return redirect('menu')

    payment_method = request.POST.get('payment_method')
    delivery_method = request.POST.get('delivery_method')
    dorm_input = request.POST.get('dorm') or request.user.userprofile.dorm_location

    user_profile = request.user.userprofile
    total_cost = sum(Decimal(item['price']) * item['quantity'] for item in cart)
    total_quantity = sum(item['quantity'] for item in cart)
    swipe_eligible = any(Meal.objects.get(id=item['meal_id']).mealSwipe for item in cart)

    if payment_method == 'meal_swipe':
        if user_profile.meal_swipes < total_quantity:
            messages.error(request, f"You only have {user_profile.meal_swipes} meal swipes left, but you are ordering {total_quantity} items.")
            return redirect('view_cart')
        user_profile.meal_swipes -= total_quantity

    elif payment_method == 'flex_dollars':
        if user_profile.flex_dollars < total_cost:
            messages.error(request, "You do not have enough flex dollars.")
            return redirect('view_cart')
        user_profile.flex_dollars -= total_cost

    user_profile.dorm_location = dorm_input
    user_profile.save()

    order = Order.objects.create(
        user=request.user,
        payment_method=payment_method,
        delivery_method=delivery_method,
        dorm_location=dorm_input,
        phone_number=user_profile.phone_number
    )

    for item in cart:
        meal = Meal.objects.get(id=item['meal_id'])
        special_request = item.get('special_request', '')
        OrderItem.objects.create(
            order=order,
            meal=meal,
            quantity=item['quantity'],
            price_at_order=item['price'],
            special_request=special_request
        )

    request.session['cart'] = []
    return redirect('order_placed', order_id=order.id)

@login_required
def edit_account(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        dorm_location = request.POST.get('dorm_location')

        user_profile = request.user.userprofile
        user_profile.phone_number = phone_number
        user_profile.dorm_location = dorm_location
        user_profile.save()

        messages.success(request, 'Profile updated successfully!')
        return redirect('edit_account')
    return render(request, 'orders/edit_account.html')

@login_required
def account(request):
    return render(request, 'orders/account.html')

@login_required
def order_history(request):
    all_orders = Order.objects.filter(user=request.user).order_by('-created_at')
    favorite_orders = all_orders.filter(favorite=True)
    return render(request, 'orders/order_history.html', {
        'all_orders': all_orders,
        'favorite_orders': favorite_orders
    })

def check_order_status(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        return JsonResponse({'status': order.status})
    except Order.DoesNotExist:
        return JsonResponse({'status': 'error'}, status=404)

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
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order.favorite = not order.favorite
    order.save()
    return redirect('order_details', order_id=order_id)

@login_required
def reorder_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        return redirect('order_history')

    cart = []
    for item in order.orderitem_set.all():
        cart.append({
            'meal_id': item.meal.id,
            'name': item.meal.name,
            'price': float(item.meal.price),
            'side': item.meal.side,
            'quantity': item.quantity,
            'special_request': item.special_request,
            'image': item.meal.image.url if item.meal.image else None,
        })
    request.session['cart'] = cart
    return redirect('view_cart')

def order_placed(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order_placed.html', {'order': order})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('menu')
    else:
        form = CustomUserCreationForm()
    return render(request, 'orders/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('menu')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

# Cart count 
def get_cart_count(request):
    cart = request.session.get('cart', [])
    return JsonResponse({'count': len(cart)})

# Triton Service views

def is_admin(user):
    return user.is_superuser or user.is_staff

@user_passes_test(is_admin)
def triton_service(request):
    orders = Order.objects.all()
    dorm = request.GET.get('dorm', '').strip()
    status = request.GET.get('status', '').strip()
    delivery_method = request.GET.get('delivery_method', '').strip()
    ordering = request.GET.get('ordering', '-created_at')  # Default to most recent orders

    if dorm:
        orders = orders.filter(dorm_location__icontains=dorm)
    if status:
        orders = orders.filter(status__iexact=status)
    if delivery_method:
        orders = orders.filter(delivery_method=delivery_method)

    # Apply ordering
    orders = orders.order_by(ordering)

    context = {
        'orders': orders,
        'STATUS_DISPLAY': {
            'pending': 'Pending',
            'ready_for_pickup': 'Ready for Pickup',
            'on_the_way': 'On the Way',
            'delivered': 'Delivered',
            'canceled': 'Canceled',
        }
    }
    return render(request, 'orders/triton_service.html', context)

@user_passes_test(is_admin)
def update_order_status(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        new_status = request.POST.get('status')
        if new_status:
            if new_status.lower() == 'canceled' and order.status.lower() != 'canceled':
                if order.payment_method == 'meal_swipe':
                    order.user.userprofile.meal_swipes += 1
                elif order.payment_method == 'flex_dollars':
                    total = sum(i.quantity * i.price_at_order for i in order.orderitem_set.all())
                    order.user.userprofile.flex_dollars += total
                order.user.userprofile.save()
            order.status = new_status
            order.save()
            messages.success(request, f"Order {order.id} updated to '{new_status}'")
    return redirect('triton_service')

def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            new_password = form.cleaned_data.get('new_password')

            try:
                user = User.objects.get(username=username)
                user.set_password(new_password)
                user.save()
                messages.success(request, "Password has been reset successfully. You can now log in with your new password.")
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, "User not found.")
    else:
        form = PasswordResetForm()

    return render(request, 'registration/password_reset.html', {'form': form})