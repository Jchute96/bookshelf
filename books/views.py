from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Book
from .forms import EditBookForm



# Create your views here.

# Display books
def home(request):
    # Retrieve all books from database
    books = Book.objects.all()
    
    # Get all unique years for the filter dropdown
    years = Book.objects.dates('date_finished', 'year', order='DESC')
    
    #Apply the filters if selected
    
    genre = request.GET.get('genre')
    # If user submitted a genre to filter by
    if genre:
        books = books.filter(genre=genre)
    
    rating = request.GET.get('rating')
    # If user submitted a rating to filter by
    if rating:
        books = books.filter(rating=rating)
    
    year = request.GET.get('year')
    # If user submitted a year to filter by
    if year:
        books = books.filter(date_finished__year=year)
    
        
    context = {'books': books, 'years': years}
    return render(request, 'books/home.html', context)

# List a single book and take a books id as an argument
def book_detail(request, id):
    # Query a book by its id
    book = Book.objects.get(pk=id)
    context = {'book': book}
    return render(request, 'books/book-detail.html', context)

# Add a book
def add_book(request):
    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('image')
        date_finished = data.get('date_finished') or None
        purchase_link = data.get('purchase_link') or None
        
        book = Book.objects.create(
            title = data['title'],
            author = data['author'],
            genre = data['genre'],
            rating = data['rating'],
            review = data['review'],
            purchase_link = purchase_link,
            date_finished = date_finished,
            image = image
        )
        
        return redirect('home')
    
    return render(request, 'books/add-book.html')

# Edit a book's info and takes id as an argument
def edit_book(request, id):
    # Get book to update
    book = Book.objects.get(pk=id)
    
    form = EditBookForm(instance=book)
    
    if request.method == 'POST':
        # Fill form with requested data
        form = EditBookForm(request.POST, request.FILES, instance=book)
        
        if form.is_valid():
            # Save data to database
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'books/update-book.html', context)

# Delete a book, takes id as argument
def delete_book(request, id):
    book = Book.objects.get(pk=id)
    if request.method == 'POST':
        book.delete()
        return redirect('home')
    
    context = {'book': book}
    return render(request, 'books/delete-book.html', context)



