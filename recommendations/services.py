from django.db.models import Count
from books.models import Book
from books.services import search_google_books


def generate_recommendations(user):
    
    # Find the users finished books
    finished_books = Book.objects.filter(user=user, status='finished')
    
    # Make sure user has at least 5 finished books we can use to form recommendations
    if len(finished_books) < 5:
        return None
    
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
                    recommendations.append(result)
            
    return recommendations
    