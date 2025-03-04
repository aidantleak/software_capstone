from django.db import models

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