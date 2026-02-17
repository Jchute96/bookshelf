from django.shortcuts import render, redirect
from django.http import response, HttpResponse
from .models import BookList
from books.models import Book
from django.contrib.auth.decorators import login_required
from .forms import CreateListForm, EditListForm
from django.template.loader import render_to_string
from weasyprint import HTML
import csv

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
    
    # Get the books to use for the list images
    finished_books = books.filter(status='finished')[:4]
    currently_reading_books = books.filter(status='currently_reading')[:4]
    want_to_read_books = books.filter(status='want_to_read')[:4]
    
    
    
    context = {
        'lists': lists, 
        'finished_count': finished_count, 
        'currently_reading_count': currently_reading_count, 
        'want_to_read_count': want_to_read_count,
        'finished_books': finished_books,
        'currently_reading_books': currently_reading_books,
        'want_to_read_books': want_to_read_books
    }
    
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
    
            

@login_required
def edit_list(request, list_id):
    
    # Get the list that will have its name changed
    user_list = BookList.objects.get(pk=list_id, user=request.user)
    
    # If user submits the edit form
    if request.method == 'POST':
        
        #  Create and fill customized form for this specific user list
        form = EditListForm(request.POST, instance=user_list)
        
        # Verify the user entered data is valid
        if form.is_valid():
            
            # Save the new list name
            form.save()
            
            # Redirect to main lists page
            return redirect('list-detail', list_id=list_id)
    
    # Display form
    else:
        form = EditListForm(instance=user_list)
            
    context = {'form': form, 'user_list': user_list}
    return render(request, 'lists/edit-list.html', context)
        
        
@login_required
def delete_list(request, list_id):
    
    user_list = BookList.objects.get(pk=list_id, user=request.user)
    
    if request.method == 'POST':
        user_list.delete()
        return redirect('my-lists')
    
    context = {'user_list': user_list}
    return render(request, 'lists/delete-list.html', context)


@login_required
def essential_list(request, status):
    
    books = Book.objects.filter(status=status, user=request.user)
    
    status_names = {
        'finished': 'Finished',
        'currently_reading': 'Currently Reading',
        'want_to_read': 'Want to Read'
    }
    
    # Assign the list name the value of the status depending on what the user clicks
    list_name = status_names[status]
    
    books = books.order_by('title')
    
    context = {'books': books, 'list_name': list_name, 'status': status}
    
    return render(request, 'lists/essential-list.html', context)

# Create view that takes format parameter as well as list_id and status as optional parameters
@login_required
def export_list(request, format, list_id=None, status=None):
    
    # If user is trying to export a custom list
    if list_id:
        
        # Get the current user list
        user_list = BookList.objects.get(pk=list_id, user = request.user)
        
        # Get all the books from that list
        books = user_list.books.all()
        
        # Order the books in alphabetical order
        books = books.order_by('title')
        
        # Get list name for the filename
        list_name = user_list.name
    
    # If user is trying to export a essential list
    else:
        # Get all books for the user filtered by the status value
        books = Book.objects.filter(status=status, user=request.user)
        
        # Order the books in alhabetical order
        books = books.order_by('title')
        
        status_names = {
            'finished': 'Finished',
            'currently_reading': 'Currently Reading',
            'want_to_read': 'Want to Read'
        }
        
        # Assign the list name the value of the status for the filename
        list_name = status_names[status]
           
    if format == 'csv':
        # Create a CSV response
        response = HttpResponse(content_type='text/csv')
        
        # Create a file name by replacing spaces with underscores and making it lowercase
        filename = list_name.replace(' ', '_').lower() + '.csv'
        
        # Tell browser to download file with the filename
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        # Create a CSV writer to write to the response
        writer = csv.writer(response)
        
        # Write header row for the column names
        writer.writerow(['Title', 'Author', 'Genre', 'Rating', 'Review', 'Purchase Link'])
        
        # Fill out each following row with the info from each book
        for book in books:
            writer.writerow([
                book.title,
                book.author,
                # Display the Display names for genre
                book.get_genre_display(),
                f"{book.rating}/5" if book.rating else '',
                book.review or '',
                book.purchase_link or '',
            ])
        
        # Return the HttpResponse that tells the browser to download the newly created csv file
        return response
        
    elif format == 'pdf':
        # Create a file name by replacing spaces with underscores and making it lowercase
        filename = list_name.replace(' ', '_').lower() + '.pdf'
        
        # Render the export-pdf HTML template with its context as a string
        export_HTML_string = render_to_string('lists/export-pdf.html', {'books': books, 'list_name': list_name})
        
        
        # Use WeasyPrints HTML to create an HTML object from the HTML string which acts as a blueprint
        html = HTML(string=export_HTML_string)
        # Convert the HTML object to PDF format and convert it to bytes using WeasyPrints .write_pdf method
        pdf = html.write_pdf()
        
        # Create a pdf response with the pdf data
        response = HttpResponse(pdf, content_type='application/pdf')
        # Tell browser to download file with the filename
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        # Return the HttpResponse that tells the browser to download the newly created pdf file
        return response    
        
    else:
        return HttpResponse("Invalid format. Use 'csv' or 'pdf'.", status=400)
        
        
        
        
        
    
    
    
    
      
        
        
        
        
        
        
        
          
            
            
            
            

        
        
    
    
    
    
    

