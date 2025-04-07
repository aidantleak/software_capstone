from django.contrib import admin
from .models import Meal, Order, OrderItem, UserProfile

@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'mealSwipe', 'image_preview')
    list_filter = ('category', 'mealSwipe')
    search_fields = ('name', 'category')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50"/>', obj.image.url)
        return "No Image"
    
    image_preview.short_description = 'Image Preview'
    image_preview.allow_tags = True

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'payment_method', 'delivery_method', 'created_at', 'favorite')
    list_filter = ('status', 'payment_method', 'delivery_method', 'favorite', 'created_at')
    search_fields = ('user__username',)
    list_editable = ('status', 'favorite')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'meal', 'quantity', 'price_at_order')
    search_fields = ('meal__name', 'order__id')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'meal_swipes', 'flex_dollars', 'phone_number', 'dorm_location')
    search_fields = ('user__username', 'phone_number', 'dorm_location')
