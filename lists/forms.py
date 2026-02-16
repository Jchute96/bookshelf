from .models import BookList
from django.forms import ModelForm
from django import forms

# declaring the ModelForm
class CreateListForm(ModelForm):
    
    class Meta:
        # the Model from which the form will inherit from
        model = BookList
        # Display included fields in this order on form
        fields = ['name']
        # styling the form with bootstrap classes
        widgets = {
             'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'List Name'}),
        }