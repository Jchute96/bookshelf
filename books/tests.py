from django.test import TestCase
from django.contrib.auth.models import User
from .models import Book
from django.urls import reverse

# Create your tests here.

class BookModelTests(TestCase):
    
    # Arrange, Act, Assert when doing unit tests
    # 1. Arrange - set up objects/data
    # 2. Act - execute the specific behavior under test
    # 3. Assert - verify the expected outcome
    
    # Arrange - use setUp to set up the test objects/data which runs before every test method automatically
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.book = Book.objects.create(
            user=self.user,
            title='Test Book',
            author='Test Author',
            status='finished',
            genre='fiction',
            rating=3
        )
        
    def test_get_star_display_three_stars(self):
        # Act
        result = self.book.get_star_display()
        # Assert
        self.assertEqual(result, '⭐⭐⭐☆☆')
    
    def test_get_star_display_no_rating(self):
        # Arrange
        self.book.rating = None
        # Act
        result = self.book.get_star_display()
        # Assert
        self.assertEqual(result, '')
    
    def test_get_star_display_one_star(self):
        # Arrange
        self.book.rating = 1
        # Act
        result = self.book.get_star_display()
        # Assert
        self.assertEqual(result, '⭐☆☆☆☆')
    
    def test_get_star_display_five_stars(self):
        # Arrange
        self.book.rating = 5
        # Act
        result = self.book.get_star_display()
        # Assert
        self.assertEqual(result, '⭐⭐⭐⭐⭐')
        
class HomeViewTests(TestCase):
    
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='testpass123')
        self.user2 = User.objects.create_user(username='user2', password='testpass123')
        
        self.user1_book = Book.objects.create(
            user=self.user1,
            title='User1 Book',
            author='Test Author',
            status='finished',
            genre='fiction'
        )
        
        self.user2_book = Book.objects.create(
            user=self.user2,
            title='User2 Book',
            author='Test Author',
            status='finished',
            genre='fiction'
        )
    
    def test_home_redirects_if_not_logged_in(self):
        
        # Act - use reverse to look up URL by its name instead of its path
        response = self.client.get(reverse('home'))
        # Assert - Check if there was a redirect to login page
        self.assertRedirects(response, '/accounts/login/?next=/books/')
        
    def test_home_loads_for_logged_in_user(self):
        # Arrange - log user in
        self.client.login(username='user1', password='testpass123')
        # Act - use reverse to look up URL by its name instead of its path
        response = self.client.get(reverse('home'))
        # Assert - Check if HTML loaded properly with correct response by searching for User1 Book in redered HTML response
        self.assertContains(response, 'User1 Book')
        
    def test_home_only_shows_users_own_books(self):
        # Arrange - log user in
        self.client.login(username='user1', password='testpass123')
        # Act
        response = self.client.get(reverse('home'))
        # Assert
        self.assertNotContains(response, 'User2 Book')

class AddBookTests(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        
    def test_add_book_creates_book_and_redirects(self):
        # Arrange
        self.client.login(username='testuser', password='testpass123')
        # Act
        response = self.client.post(reverse('add-book'), {
            'title': 'New Book',
            'author': 'New Author',
            'status': 'finished',
            'genre': 'fiction',
            'review': 'Great book!',
        })
        # Assert - Check that redirect to home happens and new book exists
        self.assertRedirects(response, '/books/')
        self.assertTrue(Book.objects.filter(title='New Book', user=self.user).exists())
        
class DeleteBookTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='testpass123')
        self.user2 = User.objects.create_user(username='user2', password='testpass123')
        
        self.user1_book = Book.objects.create(
            user=self.user1,
            title='User1 Book',
            author='Test Author',
            status='finished',
            genre='fiction'
        )
        
    # Book is removed from database and redirects to home
    def test_delete_book_deletes_book_and_redirects(self):
        # Arrange
        self.client.login(username='user1', password='testpass123')
        # Act - Try to delete the form and use the books id as an argument
        response = self.client.post(reverse('delete-book', args=[self.user1_book.id]))
        # Assert - Make sure we are redirect to home page and that the book no longer exists
        self.assertRedirects(response, '/books/')
        self.assertFalse(Book.objects.filter(pk=self.user1_book.id).exists())
        
    
    def test_delete_book_redirects_if_not_logged_in(self):
        # Act
        response = self.client.post(reverse('delete-book', args=[self.user1_book.id]))
        # Assert
        self.assertRedirects(response, f'/accounts/login/?next=/books/delete-book/{self.user1_book.id}/')
        
    def test_delete_book_cannot_delete_another_users_book(self):
        # Arrange
        self.client.login(username='user2', password='testpass123')
        # Act
        response = self.client.post(reverse('delete-book', args=[self.user1_book.id]))
        # Assert - That the user gets a 404 page response and the book still exists
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Book.objects.filter(pk=self.user1_book.id).exists())
        
class EditBookTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='testpass123')
        self.user2 = User.objects.create_user(username='user2', password='testpass123')
        
        self.user1_book = Book.objects.create(
            user=self.user1,
            title='User1 Book',
            author='Test Author',
            status='finished',
            genre='fiction'
        )
    
    def test_edit_book_edit_book_and_redirects(self):
        # Arrange 
        self.client.login(username='user1', password='testpass123')
        # Act
        response = self.client.post(reverse('edit-book', args=[self.user1_book.id]), {
            'title': 'User1 New Book',
            'author': 'Test Author',
            'status': 'finished',
            'genre': 'fiction',
            })

        # Assert
        self.assertRedirects(response, reverse('book-detail', args=[self.user1_book.id]))
        self.assertTrue(Book.objects.filter(title='User1 New Book', user=self.user1).exists())
        
    def test_edit_book_cannot_edit_another_users_book(self):
        # Arrange
        self.client.login(username='user2', password='testpass123')
        # Act - Try to edit another users book
        response = self.client.post(reverse('edit-book', args=[self.user1_book.id]), {
            'title': 'User1 New Book',
            'author': 'Test Author',
            'status': 'finished',
            'genre': 'fiction',
            })
        # Assert - The user gets a 404 response and original title has not been changed
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Book.objects.filter(title='User1 Book').exists())
   
class SearchTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.book1 = Book.objects.create(
            user=self.user,
            title='The Hobbit',
            author='J.R.R. Tolkien',
            status='finished',
            genre='fiction',
            rating=5
        )
        self.book2 = Book.objects.create(
            user=self.user,
            title='Atomic Habits',
            author='James Clear',
            status='finished',
            genre='fiction',
            rating=3
        )
        
    def test_search_by_title_returns_title(self):
        # Arrange
        self.client.login(username='testuser', password='testpass123')
        # Act
        response = self.client.get(reverse('home'), {'search': 'Hobbit'})
        # Assert
        self.assertContains(response, 'The Hobbit')
        self.assertNotContains(response, 'Atomic Habits')
        
    def test_search_by_author_returns_author(self):
        # Arrange
        self.client.login(username='testuser', password='testpass123')
        # Act
        response = self.client.get(reverse('home'), {'search': 'James'})
        # Assert
        self.assertContains(response, 'James Clear')
        self.assertNotContains(response, 'J.R.R. Tolkien')
        
    def test_search_is_case_insensitive(self):
        # Arrange
        self.client.login(username='testuser', password='testpass123')
        # Act
        response = self.client.get(reverse('home'), {'search': 'hobbit'})
        # Assert
        self.assertContains(response, 'The Hobbit')
    
    def test_search_no_results_for_search_that_doesnt_exist(self):
        # Arrange
        self.client.login(username='testuser', password='testpass123')
        # Act
        response = self.client.get(reverse('home'), {'search': 'alchemist'})
        # Assert
        self.assertNotContains(response, 'The Hobbit')
        self.assertNotContains(response, 'Atomic Habits')
        

class FilterTests(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.book1 = Book.objects.create(
            user=self.user,
            title='The Hobbit',
            author='J.R.R. Tolkien',
            status='finished',
            genre='fiction',
            rating=5,
            date_finished='2024-01-01'
        )
        self.book2 = Book.objects.create(
            user=self.user,
            title='Atomic Habits',
            author='James Clear',
            status='finished',
            genre='nonfiction',
            rating=3,
            date_finished='2023-01-01'
        )
        self.book3 = Book.objects.create(
            user=self.user,
            title='The Alchemist',
            author='Paulo Coelho',
            status='want_to_read',
            genre='fiction',
        )
        
    def test_filter_by_genre(self):
        # Arrange
        self.client.login(username='testuser', password='testpass123')
        # Act
        response = self.client.get(reverse('home'), {'genre': 'fiction'})
        # Assert
        self.assertContains(response, 'The Hobbit')
        self.assertContains(response, 'The Alchemist')
        self.assertNotContains(response, 'Atomic Habits')
        
    def test_filter_by_status(self):
        # Arrange
        self.client.login(username='testuser', password='testpass123')
        # Act
        response = self.client.get(reverse('home'), {'status': 'finished'})
        # Assert
        self.assertContains(response, 'The Hobbit')
        self.assertContains(response, 'Atomic Habits')
        self.assertNotContains(response, 'The Alchemist')
        
    def test_filter_by_rating(self):
        # Arrange
        self.client.login(username='testuser', password='testpass123')
        # Act
        response = self.client.get(reverse('home'), {'rating': '5'})
        # Assert
        self.assertContains(response, 'The Hobbit')
        self.assertNotContains(response, 'Atomic Habits')
        self.assertNotContains(response, 'The Alchemist')
    
    def test_filter_by_year(self):
        # Arrange
        self.client.login(username='testuser', password='testpass123')
        # Act
        response = self.client.get(reverse('home'), {'year': '2024'})
        # Assert
        self.assertContains(response, 'The Hobbit')
        self.assertNotContains(response, 'Atomic Habits')
        
        
class StatisticsTests(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        # Four 5-star finished books with different dates
        self.book1 = Book.objects.create(
            user=self.user,
            title='The Hobbit',
            author='J.R.R. Tolkien',
            status='finished',
            genre='fiction',
            rating=5,
            date_finished='2024-01-04'
        )
        self.book2 = Book.objects.create(
            user=self.user,
            title='Atomic Habits',
            author='James Clear',
            status='finished',
            genre='nonfiction',
            rating=5,
            date_finished='2024-01-03'
        )
        self.book3 = Book.objects.create(
            user=self.user,
            title='The Alchemist',
            author='Paulo Coelho',
            status='finished',
            genre='fiction',
            rating=5,
            date_finished='2024-01-02'
        )
        self.book4 = Book.objects.create(
            user=self.user,
            title='1984',
            author='George Orwell',
            status='finished',
            genre='fiction',
            rating=5,
            date_finished='2024-01-01'
        )
        
        # Lower rated book that makes it so avg is just not all 5s
        self.book5 = Book.objects.create(
            user=self.user,
            title='Deep Work',
            author='Cal Newport',
            status='finished',
            genre='selfhelp',
            rating=3,
            date_finished='2023-01-01'
        )

        # Should not count in statistics
        self.book6 = Book.objects.create(
            user=self.user,
            title='The Winds of Winter',
            author='George R.R. Martin',
            status='want_to_read',
            genre='fantasy',
        )
        
    def test_statistics_total_books_only_counts_finished_books(self):
        # Arrange
        self.client.login(username='testuser', password='testpass123')
        # Act
        response = self.client.get(reverse('statistics'))
        # Assert
        self.assertEqual(response.context['total_books'], 5)
        
    def test_statistics_avg_rating_calculated_correctly(self):
        # Arrange
        self.client.login(username='testuser', password='testpass123')
        # Act
        response = self.client.get(reverse('statistics'))
        # Assert
        self.assertEqual(response.context['avg_rating'], 4.6)
        
    def test_statistics_avg_rating_is_0_when_no_finished_books(self):
        # Arrange - Create a new user with no books and sign them in
        new_user = User.objects.create_user(username='newuser', password='testpass123')
        self.client.login(username='newuser', password='testpass123')
        # Act - Get statistics page HTML response which should return 0 for avg
        response = self.client.get(reverse('statistics'))
        # Assert - Make sure that the avg_rating is 0
        self.assertEqual(response.context['avg_rating'], 0)
        
    
    def test_statistics_display_only_top3_recent_5star_books(self):
        # Arrange
        self.client.login(username='testuser', password='testpass123')
        # Act - Get the top3 recent books from the response
        response = self.client.get(reverse('statistics'))
        top3 = response.context['top3_recent_books']
        # Assert - Make sure that the top 3 length is right and that oldest top5 book is not included in the top 3
        self.assertEqual(len(top3), 3)
        self.assertIn(self.book1, top3)
        self.assertIn(self.book2, top3)
        self.assertIn(self.book3, top3)
        self.assertNotIn(self.book4, top3)
        
    def test_statistics_display_only_top3_books_with_date(self):
        # Arrange
        new_user2 = User.objects.create_user(username='newuser2', password='testpass123')
        self.client.login(username='newuser2', password='testpass123')
        
        fave_book = Book.objects.create(
            user=new_user2,
            title='Meditations',
            author='Marcus Aurelius',
            status='finished',
            genre='selfhelp',
            rating=5,
            date_finished='2024-02-01'
        )
        fave_book_without_date = Book.objects.create(
            user=new_user2,
            title='Steve Jobs',
            author='Walter Isaacson',
            status='finished',
            genre='biography',
            rating=5
        )
        book_with_4stars = Book.objects.create(
            user=new_user2,
            title='The Da Vinci Code',
            author='Dan Brown',
            status='finished',
            genre='mystery',
            rating=4,
            date_finished='2024-01-02'
        )
        
        # Act
        response = self.client.get(reverse('statistics'))
        top3 = response.context['top3_recent_books']
        
        # Assert
        self.assertIn(fave_book, top3)
        self.assertNotIn(fave_book_without_date, top3)
        self.assertNotIn(book_with_4stars, top3)