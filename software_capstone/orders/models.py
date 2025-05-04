from django.db import models
from django.contrib.auth.models import User  

class SideChoices(models.TextChoices):
    FRIES = 'fries', 'Fries'
    SWEET_POTATO_FRIES = 'sweet_potato_fries', 'Sweet Potato Fries'
    CHIPS = 'chips', 'Chips'
    FRUIT = 'fruit', 'Fruit'


class mealCategories(models.TextChoices):
    BREAKFAST = 'breakfast', 'Breakfast'
    Entree = 'entree', 'Entree'
    Appetizer = 'appetizer', 'Appetizer'
    Dessert = 'dessert', 'Dessert'
    Beverage = 'beverage', 'Beverage'
    Side = 'side', 'Side'
    Other = 'other', 'Other'

class Meal(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    side = models.CharField(
        max_length=50,
        choices=SideChoices.choices,  # Adds the dropdown choices
        default=SideChoices.FRIES
    )
    category = models.CharField(
        max_length=50,
        choices=mealCategories.choices,  # Adds the dropdown choices
        default=mealCategories.Entree

    )
    image = models.ImageField(upload_to='menu_images/', null=True, blank=True)
    mealSwipe = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.get_side_display()}"  
    


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('preparing', 'Preparing'),
            ('completed', 'Completed'),
        ],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)  # Time when order is placed

    def __str__(self):
        return f"Order {self.id} by {self.user.username if self.user else 'Guest'}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)  # Links to an order
    meal = models.ForeignKey('Meal', on_delete=models.CASCADE)  # Links to a meal
    quantity = models.PositiveIntegerField(default=1)  # Stores quantity of the meal
    price_at_order = models.DecimalField(max_digits=6, decimal_places=2)  # Stores price at purchase time

    def __str__(self):
        return f"{self.quantity} x {self.meal.name} in Order {self.order.id}"
    

