from django.contrib import admin
from .models import *

@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'image_preview', 'mealSwipe')  # Adds a column with the image preview
    list_filter = ('category', 'mealSwipe')  # Adds a filter
    search_fields = ('name', 'category', 'meal swipe')  # Adds a search bar

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="50"/>'
        return "No Image"
    
    image_preview.allow_tags = True
    image_preview.short_description = 'Image'
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'created_at', 'favorite')
    list_filter = ('status', 'favorite', 'created_at')
    search_fields = ('user__username',)
    list_editable = ('status', 'favorite')