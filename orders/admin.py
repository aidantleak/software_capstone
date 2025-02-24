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