import anthropic
import json
from django.db.models import Count
from books.models import Book
from books.services import search_google_books

# Checks if user has enough books for recommendations
def has_enough_books(user):
    return Book.objects.filter(user=user, status='finished').count() >= 5

def generate_recommendations(user):
    
    if not has_enough_books(user):
        return None
    
    finished_books = Book.objects.filter(user=user, status='finished')

    # Group all of the authors and count how many books user has read for them. Order authors by authors with most books read and only store top 3
    favorite_authors = finished_books.values('author').annotate(count = Count('id')).order_by('-count')[:3]
    
    # Get a simple list of all the titles of the books the user has read, already wants to read, or is currently reading
    seen_books = Book.objects.filter(user=user).values_list('title', flat=True)
    
    # List to keep track of recommendations
    recommendations = []
    
    # Iterate through the authors and use google books api to find books not in seen_books
    for author in favorite_authors:
        
        # Get ther results from google books api search by author
        results = search_google_books(author['author'])
        
        # If the results are not none add them to recommendations list
        if results:
            
            for result in results[:2]:
                if result['title'] not in seen_books:
                    
                    # Store the favorite author in the results to use to display
                    result['searched_author'] = author['author']
                    recommendations.append(result)
            
    return recommendations


def get_claude_recommendations(user):
    
    # If user has fewer than 5 finished books return None
    if not has_enough_books(user):
        return None
    
    # These are all the books associated with the users account such as finished, want to read, and currently reading books
    all_books = Book.objects.filter(user=user)
    
    finished_books = all_books.filter(status='finished')
    
    # Get top 10 books from the users finished books and store each book's title, author, genre, and rating 
    favorite_books = finished_books.values('title', 'author', 'genre', 'rating').order_by('-rating')[:10]
    
    # Get top 3 user genres using annotate to count the number of book id's associated with each genre
    favorite_genres = finished_books.values('genre').annotate(count = Count('id')).order_by('-count')[:3]
    
    # Get top 3 Authors using annotate to count the number of book id's associated with each author
    favorite_authors = finished_books.values('author').annotate(count = Count('id')).order_by('-count')[:3]
    
    # This will be used to store the different lines of text for our prompt to claude
    favorite_books_lines = []
    
    # Store the book data as lines in the favorite books lines list to use later for our prompt
    for book in favorite_books:
        
        if book['rating']:
            rating_text = f" {book['rating']} stars"
        else:
            rating_text = ""
        
        favorite_books_lines.append(f"- \"{book['title']}\" by {book['author']} ({book['genre']}{rating_text})")
        
    favorite_books_text = '\n'.join(favorite_books_lines)
    
    # Map genre keys to their readable labels for the prompt
    genre_labels = dict(Book.GENRE_CHOICES)

    # Goes through all of users favorite genres and stores just the genre values in genre_text with a comma separating them
    genres_text = ', '.join([genre_labels.get(genre['genre'], genre['genre']) for genre in favorite_genres])
    
    # Goes through all of users favorite authors and stores just the author values in authors_text with a comma separating them
    authors_text = ', '.join([author['author'] for author in favorite_authors])
    
    # Store all the titles of all of the users books separated by commas
    seen_books_text = ', '.join(all_books.values_list('title', flat=True))
    
    # System prompt tells Claude who it is and the rules it must follow
    system_prompt = '''You are a book recommendation assistant.
    Recommend books that genuinely exist and are widely available.
    For the reason field, explain specifically why this book matches the user's taste based on their genres or authors.
    Return only a JSON array like this:
    [{"title": "...", "author": "...", "reason": "..."}]
    No other text, no markdown, no code blocks.'''

    # User prompt holds the users data for claude to review
    user_prompt = f'''Books the user has read:
    {favorite_books_text}

    Favorite genres: {genres_text}
    Favorite authors: {authors_text}

    Do not recommend these books: {seen_books_text}

    Recommend 6 books this user would enjoy based on their reading history, favorite genres, and favorite authors.'''

    # Format for making the api call to Claude, by prefilling '[' in it it forces Claude to start its response in the JSON array
    client = anthropic.Anthropic()

    # Try making the api call and if it fails return None
    try:
        message = client.messages.create(
            model='claude-haiku-4-5-20251001',
            max_tokens=1024,
            system=system_prompt,
            messages=[
                {'role': 'user', 'content': user_prompt},
                {'role': 'assistant', 'content': '['},
            ]
        )
    except anthropic.APIError:
        return None

    # Pre-fill starts the response with '[', so we prepend it back before parsing
    try:
        recommendations = json.loads('[' + message.content[0].text)
    
    # If parsing fails return None
    except json.JSONDecodeError:
        return None
    
    # After getting the data from claude use it with the google books api to get cover images and purchase link if they exist
    for recommendation in recommendations:
        
        # Build the search query to use for the google books api search using the returned recommendations title and author
        search_query = f"{recommendation['title']} {recommendation['author']}"
    
        # Call search_google_books with the query
        results = search_google_books(search_query)
    
        # If the results exist and are not empty get the first image and purchase link
        
        if results and len(results) > 0:
            
            # image and purchase_link to recommendation
            recommendation['cover_link'] = results[0]['image']
            recommendation['purchase_link'] = results[0]['purchase_link']
            
        else:
            
            # Set them to None if nothing came back
            recommendation['cover_link'] = None
            recommendation['purchase_link'] = None
    
    return recommendations