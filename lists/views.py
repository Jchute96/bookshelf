from django.shortcuts import render, redirect
from django.http import response
from .models import BookList
from books.models import Book
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def my_lists(request):
    
    # Get all lists that belong to the current user
    lists = BookList.objects.filter(user=request.user)
    
    # Get all books that belong to the current user
    books = Book.objects.filter(user=request.user)
    
    # Get the number of users finished books
    finished_count = books.filter(status='finished').count()
    
    # Get number of users currently reading books
    currently_reading_count = books.filter(status='currently_reading').count()
    
    # Get number of users want to read books
    want_to_read_count = books.filter(status='want_to_read').count()
    
    context = {'lists': lists, 'finished_count': finished_count, 'currently_reading_count': currently_reading_count, 'want_to_read_count': want_to_read_count}
    
    return render(request, 'lists/my-lists.html', context)
    
    
    
    

