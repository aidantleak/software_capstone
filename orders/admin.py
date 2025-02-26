from django.contrib import admin
from .models import Meal

@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'image_preview')
    search_fields = ('name', 'category')  # Adds a search bar

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="50"/>'
        return "No Image"
    
    image_preview.allow_tags = True
    image_preview.short_description = 'Image'
    
class Side(models.Model):
    meal = models.ForeignKey(Meal, related_name='sides', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='side_images/', null=True, blank=True)  # Optional image field
    
    
    
