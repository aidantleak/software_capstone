from django.db import models
from django.contrib.auth.models import User  
from django.contrib.auth.forms import UserCreationForm

class SideChoices(models.TextChoices):
    FRIES = 'fries', 'Fries'
    SWEET_POTATO_FRIES = 'sweet_potato_fries', 'Sweet Potato Fries'
    CHIPS = 'chips', 'Chips'
    FRUIT = 'fruit', 'Fruit'

class mealCategories(models.TextChoices):
    BREAKFAST = 'breakfast', 'Breakfast'
    ENTREE = 'entree', 'Entree'
    APPETIZER = 'appetizer', 'Appetizer'
    DESSERT = 'dessert', 'Dessert'
    BEVERAGE = 'beverage', 'Beverage'
    SIDE = 'side', 'Side'
    OTHER = 'other', 'Other'

class Meal(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    side = models.CharField(
        max_length=50,
        choices=SideChoices.choices,
        default=SideChoices.FRIES
    )
    category = models.CharField(
        max_length=50,
        choices=mealCategories.choices,
        default=mealCategories.ENTREE
    )
    image = models.ImageField(upload_to='menu_images/', null=True, blank=True)
    mealSwipe = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.get_side_display()}"  

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    meal = models.ForeignKey('Meal', on_delete=models.CASCADE)
    special_request = models.TextField(null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    side = models.CharField(max_length=50, choices=[
        ('fries', 'Fries'),
        ('sweet_potato_fries', 'Sweet Potato Fries'),
        ('chips', 'Chips'),
        ('fruit', 'Fruit'),
    ], default='fries')
    email = models.EmailField(null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('preparing', 'Preparing'),
            ('completed', 'Completed'),
            ('canceled', 'Canceled'),
        ],
        default='pending'
    )
    payment_method = models.CharField(
        max_length=20,
        choices=[
            ('meal_swipe', 'Meal Swipe'),
            ('flex_dollars', 'Flex Dollars'),
        ],
        null=True,
        blank=True
    )
    delivery_method = models.CharField(
        max_length=10,
        choices=[
            ('pickup', 'Pickup'),
            ('dorm', 'Dorm'),
        ],
        null=True,
        blank=True
    )
    dorm_location = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    favorite = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id} by {self.user.username if self.user else 'Guest'}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    meal = models.ForeignKey('Meal', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price_at_order = models.DecimalField(max_digits=6, decimal_places=2)
    special_request = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.quantity} x {self.meal.name} in Order {self.order.id}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    meal_swipes = models.IntegerField(default=250)
    flex_dollars = models.DecimalField(max_digits=6, decimal_places=2, default=150.00)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    dorm_location = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

