from django.shortcuts import render, redirect
from django.http import response
from .models import BookList
from books.models import Book
from django.contrib.auth.decorators import login_required
from .forms import CreateListForm

# Create your views here.

# Display all users lists
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

# Create a list page
@login_required
def create_list(request):
    
    # If user submits the registration form
    if request.method == 'POST':
        
        #  Create and fill customized form with the user entered data
        form = CreateListForm(request.POST)
        
        # Verify the user entered data is valid
        if form.is_valid():
            
            # Since we used ModelForm for the form we can use form.save to save it
            new_list = form.save(commit=False)
            new_list.user = request.user
            
            # Save the new list after we got the user
            new_list.save()
            
            # Redirect to main lists page
            return redirect('my-lists')
    
    # Display form
    else:
        form = CreateListForm()
            
    context = {'form': form}
    return render(request, 'lists/create-list.html', context)

# List detail page
@login_required
def list_detail(request, list_id):
    
    # Get the user list that matches the list_id
    user_list = BookList.objects.get(pk=list_id, user=request.user)
    
    # Get all books from that list
    books = user_list.books.all()
    
    context = {'user_list': user_list, 'books': books}      
    return render(request, 'lists/list-detail.html', context)
    
      
@login_required  
def add_books(request, list_id):
    
    # Get the user list that matches the list_id
    user_list = BookList.objects.get(pk=list_id, user=request.user)
    
    if request.method == 'POST':
        
        # Get the list of book ids from the form the user submitted
        selected_books = request.POST.getlist('book_ids')
        
        # Iterate through the book ids selected to add by the user
        for book in selected_books:
            # Get the book that matches the primary key taken from book_ids
            book_to_add = Book.objects.get(pk=book, user=request.user)
            
            # Add the book to the users list
            user_list.books.add(book_to_add)
    
        # Redirect to list detail page
        return redirect('list-detail', list_id=list_id)
    
    else:
        
        # Get all available books that belong to current user and are not already in list
        # Use exclude to remove books whose ID is in the list
        books = Book.objects.filter(user=request.user).exclude(id__in=user_list.books.all())
        
        # Sort the title in ascending order
        books = books.order_by('title')
        
        
    context = {'books': books, 'user_list': user_list}
    return render(request, 'lists/add-books.html', context)


@login_required
def remove_books(request, list_id):
    
    # Get the user list that matches the list_id
    user_list = BookList.objects.get(pk=list_id, user=request.user)
    
    if request.method == 'POST':
        
        # Get the list of book ids from the form the user submitted
        selected_books = request.POST.getlist('book_ids')
        
        # Iterate through the book ids selected to remove by the user
        for book in selected_books:
            # Get the book that matches the primary key taken from book_ids
            book_to_remove = Book.objects.get(pk=book, user=request.user)
            
            # Remove the book from the users list
            user_list.books.remove(book_to_remove)
    
        # Redirect to list detail page
        return redirect('list-detail', list_id=list_id)
    
    else:
        
        # Get all current books that are in the users list
        books = user_list.books.all()
        
        # Sort the title in ascending order
        books = books.order_by('title')
        
        
    context = {'books': books, 'user_list': user_list}
    return render(request, 'lists/remove-books.html', context)
    
            
            
        
        
        
        
        
        
        
        
        
        
        
          
            
            
            
            

        
        
    
    
    
    
    

