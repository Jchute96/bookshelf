from .models import Book
from django.forms import ModelForm
from django import forms

# declaring the ModelForm
class EditBookForm(ModelForm):
    
    class Meta:
        # the Model from which the form will inherit from
        model = Book
        # the fields we want from the Model
        fields = '__all__'
        # styling the form with bootstrap classes
        widgets = {
             'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Book Title'}),
             'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Author'}),
             'genre': forms.Select(attrs={'class': 'form-control'}),
             'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '5', 'placeholder': 'Rating (1-5)'}),
             'review': forms.Textarea(attrs={'class': 'form-control', 'rows': '4', 'placeholder': 'Write your review...'}),
             'date_finished': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
             'purchase_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Purchase Link'}),
             'image': forms.FileInput(attrs={'class': 'form-control'}),
        }