from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Book
from .forms import EditBookForm
from django.db.models import Count, Avg, Case, When, Value, CharField, Q
from django.db.models.functions import ExtractYear
from django.contrib.auth.decorators import login_required

# Use @login_required to make sure only logged in users can access the views

# Display books
@login_required
def home(request):
    # Retrieve all books from database that belong to the logged in user
    books = Book.objects.filter(user=request.user)
    
    # Get all unique years for the filter dropdown
    years = books.dates('date_finished', 'year', order='DESC')
    
    # Get search value if one was entered
    search = request.GET.get('search')
    
    if search:
        # If there is a search value use filter and Q objects to find titles or authors that contains the search input.
        # icontains checks if the attributes contain the search and is case insensitive.
        # Q objects allows us to filter using and, or, and not instead of just and
        books = books.filter(
            Q(title__icontains=search) | Q(author__icontains=search))
    
    #Apply the filters if selected
    
    genre = request.GET.get('genre')
    # Filter by a certain genre if selected by user
    if genre:
        books = books.filter(genre=genre)
    
    rating = request.GET.get('rating')
    # Filter by a certain rating if selected by user
    if rating:
        books = books.filter(rating=rating)
    
    year = request.GET.get('year')
    # Filter by a certain year if selected by user
    if year:
        books = books.filter(date_finished__year=year)
        
    sort = request.GET.get('sort')
    # Apply the specific sort selected by user if chosen
    match sort:
        case 'title_asc':
            books = books.order_by('title')
        case 'author_asc':
            books = books.order_by('author')
        case 'rating_desc':
            books = books.order_by('-rating')
        case 'rating_asc':
            books = books.order_by('rating')
        case 'date_desc':
            books = books.order_by('-date_finished')
        case 'date_asc':
            books = books.order_by('date_finished')
            
    # Include these variables that will be used in the templates
    context = {'books': books, 'years': years, 'genre': genre, 'rating': rating, 'year': year, 'search': search, 'sort': sort}
    return render(request, 'books/home.html', context)

# List a single book and take a books id as an argument
@login_required
def book_detail(request, id):
    # Query a book by its id
    book = Book.objects.get(pk=id)
    context = {'book': book}
    return render(request, 'books/book-detail.html', context)

# Add a book
@login_required
def add_book(request):
    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('image')
        date_finished = data.get('date_finished') or None
        purchase_link = data.get('purchase_link') or None
        
        book = Book.objects.create(
            user = request.user,
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
@login_required
def edit_book(request, id):
    # Get book to update and make sure logged in user matches the book id
    book = Book.objects.get(pk=id, user=request.user)
    
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
@login_required
def delete_book(request, id):
    # Grab the book that matches the id and belongs to the current logged in user
    book = Book.objects.get(pk=id, user=request.user)
    if request.method == 'POST':
        book.delete()
        return redirect('home')
    
    context = {'book': book}
    return render(request, 'books/delete-book.html', context)

# Displays statistics
@login_required
def statistics(request):
    #  Get all the books that belong to the current logged in user
    books = Book.objects.filter(user=request.user)
    # Get the number of total books read
    total_books = books.count()
    
    # Get the average rating of all books
    avg_rating = books.aggregate(Avg('rating'))['rating__avg']
    
    # Verify that there were ratings to average and if not set it to 0
    if avg_rating:
        avg_rating = round(avg_rating, 1)
    else:
        avg_rating = 0
        

    # Groups the books by each of their genres using .values() 
    # Use Case to create a new key/value pair for each ggenre name so we can display correct one in html later
    # then uses annotate and Count() to count the amount of id's seen for each book in each genre
    # uses Avg() to calculate the average rating for books in that genre
    # use order_by('-count') to sort by count, highest first
    genre_stats = books.values('genre').annotate(
        genre_name=Case(
            When(genre='fiction', then=Value('Fiction')),
            When(genre='nonfiction', then=Value('Non-Fiction')),
            When(genre='mystery', then=Value('Mystery')),
            When(genre='scifi', then=Value('Science Fiction')),
            When(genre='fantasy', then=Value('Fantasy')),
            When(genre='thriller', then=Value('Thriller')),
            When(genre='romance', then=Value('Romance')),
            When(genre='biography', then=Value('Biography')),
            When(genre='history', then=Value('History')),
            When(genre='selfhelp', then=Value('Self-Help')),
            output_field=CharField(),
        ), count = Count('id'), avg_rating = Avg('rating')).order_by('-count')
    
    # Group all of the authors and count how many books user has read for them. Order authors by authors with most books read and only store top 5
    author_stats = books.values('author').annotate(count = Count('id')).order_by('-count')[:5]
    
    # Filter out the books that do not have dates then use annotate and ExtractYear() to get the years from the date_finished attribute
    # Once that is done group the years by year and count how many books are associated with each year. Then order them by most recent years to least recent
    year_stats = books.filter(date_finished__isnull = False).annotate(year = ExtractYear('date_finished')).values('year').annotate(count = Count('id')).order_by('-year')
    
    # Filter books to get the books that have a 5 star rating and a date_finished then order them by most recently finished and get top 3
    top3_recent_books = books.filter(rating=5, date_finished__isnull = False).order_by('-date_finished')[:3]
    
    
    
    # Create context key value pairs to be used in the html for statistics
    context = {
        'total_books': total_books,
        'avg_rating': avg_rating,
        'genre_stats': genre_stats,
        'author_stats': author_stats,
        'year_stats': year_stats,
        'top3_recent_books': top3_recent_books
    }
    
    # Return statistics.html file filled with context data to browser
    return render(request, 'books/statistics.html', context)
    
    
    
    
    
    
    



