from .models import Book
from django.forms import ModelForm
from django import forms


class AddBookForm(ModelForm):
    
    class Meta:
        
        # the Model from which the form will inherit from
        model = Book
        
        # Display included fields in this order on form
        fields = ['title', 'author', 'genre', 'status', 'rating', 'review', 'date_finished', 'purchase_link']
        
        # Style the form
        widgets = {
             'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Book Title'}),
             'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Author'}),
             'genre': forms.Select(attrs={'class': 'form-control'}),
             'status': forms.Select(attrs={'class': 'form-control'}),
             'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '5', 'placeholder': 'Rating (1-5)'}),
             'review': forms.Textarea(attrs={'class': 'form-control', 'rows': '4', 'placeholder': 'Write your review...'}),
             'date_finished': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
             'purchase_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Purchase Link'}),
        }
        
        # Change status label to say reading status
        labels = {
            'status': 'Reading Status'
        }
        
        
# declaring the ModelForm
class EditBookForm(ModelForm):
    
    class Meta:
        
        # the Model from which the form will inherit from
        model = Book
        
        # Display included fields in this order on form
        fields = ['title', 'author', 'genre', 'status', 'rating', 'review', 'date_finished', 'purchase_link', 'image']
        
        # styling the form with bootstrap classes
        widgets = {
             'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Book Title'}),
             'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Author'}),
             'genre': forms.Select(attrs={'class': 'form-control'}),
             'status': forms.Select(attrs={'class': 'form-control'}),
             'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '5', 'placeholder': 'Rating (1-5)'}),
             'review': forms.Textarea(attrs={'class': 'form-control', 'rows': '4', 'placeholder': 'Write your review...'}),
             'date_finished': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
             'purchase_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Purchase Link'}),
             'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
        
        # Change status label to say reading status
        labels = {
            'status': 'Reading Status'
        }