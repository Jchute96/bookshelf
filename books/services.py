import os
import requests
import cloudinary.uploader

def upload_image_to_cloudinary(image_url):
    
    # Try to use image url to upload to cloudinary
    try:
                
        # Upload image to Cloudinary and store the public_id so backend can build url
        cloudinary_result = cloudinary.uploader.upload(image_url, folder='media/images')
        image = cloudinary_result['public_id'].removeprefix('media/')
            
    # If it fails use no image
    except Exception:
        image = None
    
    return image
    
def search_google_books(search):
    # Get the google api key used to connect to google books
    api_key = os.environ.get('GOOGLE_BOOKS_API_KEY')
    
    try:
        # Make a GET Request book to the google books api using the api key and the users search query
        response = requests.get(f'https://www.googleapis.com/books/v1/volumes?q={search}&key={api_key}')
    
        # Convert the json formatted response string into a Python dictionary
        data = response.json()
    
    except Exception:
        return None
    
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
        
    return search_results