from django.test import TestCase
from django.contrib.auth.models import User
from .models import Recommendation
from django.urls import reverse
from unittest.mock import patch, MagicMock
from books.models import Book
from .services import generate_recommendations, get_claude_recommendations
import anthropic


class RecommendationsSignalTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        
        self.recommendation1 = Recommendation.objects.create(
                    user=self.user,
                    title='book1',
                    author='author1',
                    cover_link=None,
                    purchase_link=None,
                    reason="Because you enjoy books by author1"  
                )
        self.recommendation2 = Recommendation.objects.create(
                    user=self.user,
                    title='book2',
                    author='author2',
                    cover_link=None,
                    purchase_link=None,
                    reason="Because you enjoy books by author2"  
                )
        self.recommendation3 = Recommendation.objects.create(
                    user=self.user,
                    title='book3',
                    author='author3',
                    cover_link=None,
                    purchase_link=None,
                    reason="Because you enjoy books by author3"  
                )
        self.recommendation4 = Recommendation.objects.create(
                    user=self.user,
                    title='book4',
                    author='author4',
                    cover_link=None,
                    purchase_link=None,
                    reason="Because you enjoy books by author4"  
                )
        self.recommendation5 = Recommendation.objects.create(
                    user=self.user,
                    title='book5',
                    author='author5',
                    cover_link=None,
                    purchase_link=None,
                    reason="Because you enjoy books by author5"  
                )
    
    # Recommendations are deleted when a book is saved 
    def test_signal_deletes_recommendations_when_book_saved(self):
        # Arrange
        self.client.login(username='testuser', password='testpass123')
            
        # Act
        self.client.post(reverse('add-book'), {
            'title': 'New Book',
            'author': 'New Author',
            'status': 'finished',
            'genre': 'fiction',
            'review': 'Great book!',
        })
            
        # Assert
        self.assertFalse(Recommendation.objects.filter(user=self.user).exists())


class RecommendationsGenerateRecommendationsTests(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        
        # Create 4 books for the user to use later in the tests
        self.book1 = Book.objects.create(
            user=self.user,
            title='Book1',
            author='Author1',
            status='finished',
            genre='fiction',
            rating=5,
            date_finished='2024-01-01'
        )
        self.book2 = Book.objects.create(
            user=self.user,
            title='Book2',
            author='Author1',
            status='finished',
            genre='nonfiction',
            rating=3,
            date_finished='2023-01-01'
        )
        self.book3 = Book.objects.create(
            user=self.user,
            title='Book3',
            author='Author2',
            status='finished',
            rating=4,
            genre='fiction',
        )
        self.book4 = Book.objects.create(
            user=self.user,
            title='Book4',
            author='Author3',
            status='finished',
            rating=4,
            genre='fiction',
        )
    
    # Returns None when user has fewer than 5 finished books
    def test_genereate_recommendations_returns_none_when_fewer_than_5_books(self):
        
        # Arrange - log user in
        self.client.login(username='testuser', password='testpass123')
        
        # Act - try using the generate recommendations function
        results = generate_recommendations(self.user)
        
        # Assert - when user has less than 4 books generate_recommendations returns None
        self.assertTrue(results is None)
    
    # Returns recommendations when user has 5 or more finished books   
    @patch('books.services.requests.get')
    def test_generate_recommendations_returns_recommendations_when_more_than_5_books(self, mock_get):
        
        # Arrange - create mock data for google books api search, log user in, and create a new book that way they have 5 books
        mock_response_data = {
            'items': [
                {
                    'volumeInfo': {
                        'title': 'TestBook1',
                        'authors': ['Author1'],
                        'categories': ['Fiction'],
                        'imageLinks': {
                            'thumbnail': 'http://example.com/thumbnail.jpg',
                            'smallThumbnail': 'http://example.com/small_thumbnail.jpg'
                        }
                    },
                    'saleInfo': {
                        'buyLink': 'http://example.com/buy'
                    }
                },
                {
                    'volumeInfo': {
                        'title': 'TestBook2',
                        'authors': ['Author1'],
                        'categories': ['Fiction'],
                        'imageLinks': {
                            'thumbnail': 'http://example.com/thumbnail.jpg',
                            'smallThumbnail': 'http://example.com/small_thumbnail.jpg'
                        }
                    },
                    'saleInfo': {
                        'buyLink': 'http://example.com/buy'
                    }
                }  
            ]      
        }
        
        # Make it so that for the google search books api get request the mock data is returned
        mock_get.return_value.json.return_value = mock_response_data
        
        self.client.login(username='testuser', password='testpass123')
        
        self.book5 = Book.objects.create(
            user=self.user,
            title='Book5',
            author='Author2',
            status='finished',
            genre='fiction',
            rating=5,
        )
        
        # Act - try using the generate recommendations function
        results = generate_recommendations(self.user)
        
        # Assert - that TestBook1 and TestBook2 are returned by generate recommendations
        self.assertEqual(results[0]['title'], 'TestBook1')
        self.assertEqual(results[0]['authors'], 'Author1')
        self.assertEqual(results[1]['title'], 'TestBook2')
        self.assertEqual(results[1]['authors'], 'Author1')
        
    # Excludes books the user has already seen
    @patch('books.services.requests.get')
    def test_generate_recommendations_excludes_books_user_has_already_seen(self, mock_get):
        
        # Arrange - create mock data of books uer has already seen before, log user in, and create a two more books of different statuses
        mock_response_data = {
            'items': [
                {
                    'volumeInfo': {
                        'title': 'Book1',
                        'authors': ['Author1'],
                        'categories': ['Fiction'],
                        'imageLinks': {
                            'thumbnail': 'http://example.com/thumbnail.jpg',
                            'smallThumbnail': 'http://example.com/small_thumbnail.jpg'
                        }
                    },
                    'saleInfo': {
                        'buyLink': 'http://example.com/buy'
                    }
                },
                {
                    'volumeInfo': {
                        'title': 'TestBook1',
                        'authors': ['Author1'],
                        'categories': ['Fiction'],
                        'imageLinks': {
                            'thumbnail': 'http://example.com/thumbnail.jpg',
                            'smallThumbnail': 'http://example.com/small_thumbnail.jpg'
                        }
                    },
                    'saleInfo': {
                        'buyLink': 'http://example.com/buy'
                    }
                }  
            ]      
        }
        
        # Make it so that for the google search books api get request the mock data is returned
        mock_get.return_value.json.return_value = mock_response_data
        
        self.client.login(username='testuser', password='testpass123')
        
        self.book5 = Book.objects.create(
            user=self.user,
            title='Book5',
            author='Author2',
            status='finished',
            genre='fiction',
            rating=5,
        )
        
        # Act - try using the generate recommendations function
        results = generate_recommendations(self.user)
        
        # Get all the titles that are in the results
        titles = [result['title'] for result in results]

        
        # Assert - that Book1 is not in the titles of the results and TestBook1 is in the results
        self.assertNotIn('Book1', titles)
        self.assertEqual(results[0]['title'], 'TestBook1')
        

class RecommendationsViewTests(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        
        self.recommendation1 = Recommendation.objects.create(
                    user=self.user,
                    title='book1',
                    author='author1',
                    cover_link=None,
                    purchase_link=None,
                    reason="Because you enjoy books by author1"  
                )
        self.recommendation2 = Recommendation.objects.create(
                    user=self.user,
                    title='book2',
                    author='author2',
                    cover_link=None,
                    purchase_link=None,
                    reason="Because you enjoy books by author2"  
                )
        self.recommendation3 = Recommendation.objects.create(
                    user=self.user,
                    title='book3',
                    author='author3',
                    cover_link=None,
                    purchase_link=None,
                    reason="Because you enjoy books by author3"  
                )
        self.recommendation4 = Recommendation.objects.create(
                    user=self.user,
                    title='book4',
                    author='author4',
                    cover_link=None,
                    purchase_link=None,
                    reason="Because you enjoy books by author4"  
                )
        self.recommendation5 = Recommendation.objects.create(
                    user=self.user,
                    title='book5',
                    author='author5',
                    cover_link=None,
                    purchase_link=None,
                    reason="Because you enjoy books by author5"  
                )
        
    # Cached recommendations are displayed without regenerating  
    def test_recommendations_displayed_without_regenerating(self):
        
        # Arrange - log user in
        self.client.login(username='testuser', password='testpass123')
        
        # Act - use reverse to look up URL by its name and get the URLs response
        response = self.client.get(reverse('my-recommendations'))
        
        # Assert - that the HTML loaded properly with the recommendations displayed on the page
        self.assertContains(response, 'book1')
        self.assertContains(response, 'book2')
        self.assertContains(response, 'book3')
        self.assertContains(response, 'book4')
        self.assertContains(response, 'book5')
    
    # Cold start shows not_enough_books message 
    def test_recommendations_display_info_message_when_user_has_less_than_5_books(self):
        
        # Arrange - create a new user with no books or recommendations to log in
        User.objects.create_user(username='testuser1', password='testpass123')
        
        self.client.login(username='testuser1', password='testpass123')
        
        # Act - use reverse to look up URL by its name and get the URLs response
        response = self.client.get(reverse('my-recommendations'))
        
        # Assert - that there is a message displayed to user telling them to add more books to get recommendations
        self.assertContains(response, 'Read and finish at least 5 books to get personalized recommendations.')
        
    # Empty recommendations list shows no recommendations message
    @patch('recommendations.views.generate_recommendations')
    def test_recommendations_displays_no_recommendations_message_when_api_returns_no_results(self, mock_generate):

        # Arrange - mock generate_recommendations to return empty list simulating API failure, log in a new user
        mock_generate.return_value = []
        User.objects.create_user(username='testuser1', password='testpass123')
        self.client.login(username='testuser1', password='testpass123')

        # Act
        response = self.client.get(reverse('my-recommendations'))

        # Assert - that the no recommendations message is displayed
        self.assertContains(response, 'No recommendations to display at this time.')
        

class GetClaudeRecommendationsTests(TestCase):

    def setUp(self):
        
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        
         # Create 5  books for the user to use later in the tests
        self.book1 = Book.objects.create(
            user=self.user,
            title='Book1',
            author='Author1',
            status='finished',
            genre='fiction',
            rating=5,
            date_finished='2024-01-01'
        )
        self.book2 = Book.objects.create(
            user=self.user,
            title='Book2',
            author='Author1',
            status='finished',
            genre='nonfiction',
            rating=3,
            date_finished='2023-01-01'
        )
        self.book3 = Book.objects.create(
            user=self.user,
            title='Book3',
            author='Author2',
            status='finished',
            rating=4,
            genre='fiction',
        )
        self.book4 = Book.objects.create(
            user=self.user,
            title='Book4',
            author='Author3',
            status='finished',
            rating=4,
            genre='fiction',
        )
        self.book5 = Book.objects.create(
            user=self.user,
            title='Book5',
            author='Author4',
            status='finished',
            rating=4,
            genre='fiction',
        )
         
    @patch('recommendations.services.anthropic.Anthropic')
    @patch('recommendations.services.search_google_books')
    def test_returns_recommendations_on_success(self, mock_google, mock_anthropic):
        
        # Arrange - set up the mock responses
        
        # MagicMock creates a fake object that mimics the anthropic client so we can control what it returns without making api calls
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client
        mock_client.messages.create.return_value.content[0].text = '{"title": "Recommended Book", "author": "Recommended Author", "reason": "Matches your taste"}]'
        
        mock_google.return_value = [
            {
                'title': 'Recommended Book',
                'authors': 'Recommended Author',
                'genres': ['Fiction'],
                'image': 'http://example.com/image.jpg',
                'small_image': 'http://example.com/small.jpg',
                'purchase_link': 'http://example.com/buy'
            }
        ]

        # Act
        results = get_claude_recommendations(self.user)

        # Assert - that the recommendations list is returned with the correct data,
        # and that the cover and purchase links from Google Books were attached
        self.assertIsNotNone(results)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], 'Recommended Book')
        self.assertEqual(results[0]['author'], 'Recommended Author')
        self.assertEqual(results[0]['cover_link'], 'http://example.com/image.jpg')
        self.assertEqual(results[0]['purchase_link'], 'http://example.com/buy')

    @patch('recommendations.services.anthropic.Anthropic')
    def test_returns_none_on_api_failure(self, mock_anthropic):

        # Arrange - set up a mock client and make messages.create raise an APIConnectionError
        # to simulate the anthropic api being unreachable
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client
        mock_client.messages.create.side_effect = anthropic.APIConnectionError(request=MagicMock())

        # Act
        results = get_claude_recommendations(self.user)

        # Assert - that None is returned so the view can fall back to Google Books
        self.assertIsNone(results)

    @patch('recommendations.services.anthropic.Anthropic')
    def test_returns_none_on_invalid_json(self, mock_anthropic):

        # Arrange - make Claude return a response that can't be parsed as JSON
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client
        mock_client.messages.create.return_value.content[0].text = 'this is not valid json'

        # Act
        results = get_claude_recommendations(self.user)

        # Assert - that None is returned so the view can fall back to Google Books
        self.assertIsNone(results)

    def test_returns_none_when_not_enough_books(self):

        # Arrange - create a user with no finished books
        user_without_books = User.objects.create_user(username='testuser2', password='testpass123')

        # Act
        results = get_claude_recommendations(user_without_books)

        # Assert - that None is returned since the user hasn't finished at least 5 books
        self.assertIsNone(results)