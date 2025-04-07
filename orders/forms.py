from django import forms
from .models import OrderItem, Meal, Order, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class OrderForm(forms.Form):
    meal = forms.ModelChoiceField(queryset=Meal.objects.all(), label="Select a meal")
    quantity = forms.IntegerField(min_value=1, initial=1, label="Quantity")

    def save(self, user=None):
        order = Order.objects.create(user=user)
        OrderItem.objects.create(
            order=order,
            meal=self.cleaned_data['meal'],
            quantity=self.cleaned_data['quantity'],
            price_at_order=self.cleaned_data['meal'].price
        )
        return order

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. A valid email address.')
    phone_number = forms.CharField(required=True, help_text='Required. Your phone number.')
    dorm_location = forms.CharField(required=True, help_text='Required. Your dorm location.')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'phone_number', 'dorm_location']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Create and save UserProfile at the same time
            UserProfile.objects.create(
                user=user,
                phone_number=self.cleaned_data['phone_number'],
                dorm_location=self.cleaned_data['dorm_location']
            )
        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
