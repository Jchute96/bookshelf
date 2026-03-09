from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Book
from .forms import EditBookForm
from django.db.models import Count, Avg, Case, When, Value, CharField, Q
from django.db.models.functions import ExtractYear
from django.contrib.auth.decorators import login_required
import requests
import os
import cloudinary.uploader
from datetime import date


# Use @login_required to make sure only logged in users can access the views

# Display books
@login_required
def home(request):
    # Retrieve all books from database that belong to the logged in user
    books = Book.objects.filter(user=request.user)
    
    # Get the total number of books that belong to the user
    total_books = Book.objects.filter(user=request.user).count()
    
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
    
    status = request.GET.get('status')
    # Filter by a certain status if selected by user
    if status:
        books = books.filter(status=status)
        
        
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
    context = {'books': books, 'total_books': total_books, 'years': years, 'genre': genre, 'status': status, 'rating': rating, 'year': year, 'search': search, 'sort': sort}
    return render(request, 'books/home.html', context)

# List a single book and take a books id as an argument
@login_required
def book_detail(request, id):
    # Query a book by its id otherwise get a 404 response
    book = get_object_or_404(Book, pk=id, user=request.user)
    context = {'book': book}
    return render(request, 'books/book-detail.html', context)

# Add a book
@login_required
def add_book(request):
    if request.method == 'POST':
        data = request.POST
        date_finished = data.get('date_finished') or None
        purchase_link = data.get('purchase_link') or None
        
        # If user is using a search to upload an image
        if data.get('image_url'):
            # Try to use image url to upload to cloudinary
            try:
                image_url = data.get('image_url')
                
                # Upload image to Cloudinary and store the public_id so backend can build url
                cloudinary_result = cloudinary.uploader.upload(image_url, folder='media/images')
                image = cloudinary_result['public_id'].removeprefix('media/')
            # If it fails use no image
            except Exception:
                image = None
                
        # If the user uploaded photo manually   
        else:
            image = request.FILES.get('image')

        
        book = Book.objects.create(
            user = request.user,
            title = data['title'],
            author = data['author'],
            genre = data['genre'],
            status = data['status'],
            rating = data.get('rating') or None,
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
    # Get book to update and make sure logged in user matches the book id otherwise get a 404 response
    book = get_object_or_404(Book, pk=id, user=request.user)
    
    form = EditBookForm(instance=book)
    
    if request.method == 'POST':
        # Fill form with requested data
        form = EditBookForm(request.POST, request.FILES, instance=book)
        
        if form.is_valid():
            # Save data to database
            form.save()
            # Redirect to the book detail page for the book just updated
            return redirect('book-detail', id=book.id)
        
    context = {'form': form}
    return render(request, 'books/update-book.html', context)

# Delete a book, takes id as argument
@login_required
def delete_book(request, id):
    # Grab the book that matches the id and belongs to the current logged in user otherwise get a 404 response
    book = get_object_or_404(Book, pk=id, user=request.user)
    if request.method == 'POST':
        book.delete()
        return redirect('home')
    
    context = {'book': book}
    return render(request, 'books/delete-book.html', context)

# Displays statistics
@login_required
def statistics(request):
    #  Get all the finished books that belong to the current logged in user
    books = Book.objects.filter(user=request.user).filter(status='finished')
    # Get the number of total books read
    total_books = books.count()
    
    # Get the average rating of all finished books
    avg_rating = books.aggregate(Avg('rating'))['rating__avg']
    
    # Verify that there were ratings to average and if not set it to 0
    if avg_rating:
        avg_rating = round(avg_rating, 1)
    else:
        avg_rating = 0
    
    # Get the amount of books read this year
    curr_year_book_count = books.filter(date_finished__year=date.today().year).count()
    # Get user current reading goal
    curr_reading_goal = request.user.profile.reading_goal
    
    # Determine the percentage completed out of 100 towards the users reading goal
    if curr_reading_goal:
        goal_progress = min((curr_year_book_count / curr_reading_goal) * 100, 100)
    # If no reading goal was set make sure progress is 0 so we do not divide by 0
    else:
        goal_progress = 0
    
        

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
        'top3_recent_books': top3_recent_books,
        'curr_year_book_count': curr_year_book_count,
        'curr_reading_goal': curr_reading_goal,
        'goal_progress': goal_progress,
    }
    
    # Return statistics.html file filled with context data to browser
    return render(request, 'books/statistics.html', context)

# Connect to Google Books API and get book data to use for add book feature
@login_required
def search_google_books(request):
    
    # Get the search query entered by user
    search = request.GET.get('search')
    
    # If user tries to search without typing anything then return a error response and do not make request to google api
    if not search:
        return JsonResponse({'error': 'No search query provided'}, status=400)
    
    # Get the google api key used to connect to google books
    api_key = os.environ.get('GOOGLE_BOOKS_API_KEY')
    
    # Make a GET Request book to the google books api using the api key and the users search query
    response = requests.get(f'https://www.googleapis.com/books/v1/volumes?q={search}&key={api_key}')
    
    # Convert the json formatted response string into a Python dictionary
    data = response.json()
    
    search_results = []
    
    for item in data.get('items', []):
        
        # Get sales info for purchase link
        sales_info = item.get('saleInfo', {})  
        
        volume_info = item['volumeInfo']
        
        title = volume_info.get('title')
        
        # If the book has no title skip adding it to the results
        if not title:
            continue
        
        # Join authors with ',' if there are multiple authors
        authors = ', '.join(volume_info.get('authors', []))
        
        # Get the genres for the title which is a list and may consist of multiple, or if there is none return an empty list
        genres = volume_info.get('categories', [])
        
        # Get the book images and check to make sure there is an image link and a thumbnail image otherwise return an empty dict or None
        image = volume_info.get('imageLinks', {}).get('thumbnail', None)
        
        # Get a higher quality version of the image if there is an image
        if image:
            image = image.replace('zoom=1', 'zoom=0')
            
        small_image = volume_info.get('imageLinks', {}).get('smallThumbnail', None)
        
        # Get purchase link or return None if there is not one
        purchase_link = sales_info.get('buyLink', None)
        
        # Add the book info to the search results list as a dictionary
        search_results.append({'title': title, 'authors': authors, 'genres': genres, 'image': image, 'small_image': small_image, 'purchase_link': purchase_link})
         
    # Return Json repsonse as a dictionary containing all of the book data grabbed from google api response
    return JsonResponse({'results': search_results})
    
    
    
    
    
    
    
    
    
    
    



