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

#  Inherit fields from the Model declared in the Meta
class EditUsernameForm(forms.ModelForm):
    
    class Meta:
        # The Model from which the form will inherit from
        model = User
        
        # Include username field from model
        fields = ['username']
        
        # Formats how the field is displayed for the user, form control makes the input boxes look polished and 
        # placeholder is what is displayed in the field
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter new username'})
        }
        
#  Inherit fields from the Model declared in the Meta
class EditEmailForm(forms.ModelForm):
    class Meta:
        model = User
        
        fields = ['email']
        
        # Use emailinput to validate the input the user enters
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter new email'})
        }
    
        
        
        
        
        
        