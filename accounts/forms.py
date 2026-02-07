from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Class that inherits Django's built in form inheriting all features and security measures
class CustomUserCreationForm(UserCreationForm):
    
    # Create an email field for the form to use and make it required
    email = forms.EmailField(required=True)
    
    
    class Meta:
        # The Model from which the form will inherit from
        model = User
        
        # Fields to include in the form
        fields = ['username', 'email', 'password1', 'password2']
        
        
        
        
        
        