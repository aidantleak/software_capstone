from django import forms
from .models import OrderItem, Meal, Order
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class OrderForm(forms.Form):
    meal = forms.ModelChoiceField(
        queryset=Meal.objects.all(), 
        label="Select a meal"
    )
    quantity = forms.IntegerField(
        min_value=1, 
        initial=1, 
        label="Quantity"
    )

    def save(self, user=None):
        # Saving the order and linking it to the user if logged in
        order = Order.objects.create(user=user)  # Creating order
        OrderItem.objects.create(
            order=order,
            meal=self.cleaned_data['meal'],
            quantity=self.cleaned_data['quantity'],
            price_at_order=self.cleaned_data['meal'].price  # Store meal price paid
        )
        return order

    
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Inform a valid email address.')

    
