from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import BookList
from books.models import Book


class CreateListTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')

   
    def test_create_list_creates_list_and_redirects(self):
        # Arrange
        self.client.login(username='testuser', password='testpass123')
        # Act
        response = self.client.post(reverse('create-list'), {
            'name': 'My Favourite Books',
        })
        # Assert
        self.assertRedirects(response, reverse('my-lists'))
        self.assertTrue(BookList.objects.filter(name='My Favourite Books', user=self.user).exists())


class DeleteListTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.user_list = BookList.objects.create(user=self.user, name='My List')

    # List is deleted from database and redirects to my-lists
    def test_delete_list_deletes_list_and_redirects(self):
        # Arrange
        self.client.login(username='testuser', password='testpass123')
        # Act
        response = self.client.post(reverse('delete-list', kwargs={'list_id': self.user_list.id}))
        # Assert
        self.assertRedirects(response, reverse('my-lists'))
        self.assertFalse(BookList.objects.filter(pk=self.user_list.id).exists())


class AddRemoveBooksTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.user_list = BookList.objects.create(user=self.user, name='My List')
        self.book = Book.objects.create(
            user=self.user,
            title='The Hobbit',
            author='J.R.R. Tolkien',
            status='finished',
            genre='fiction',
        )

    
    def test_add_book_to_list(self):
        # Arrange
        self.client.login(username='testuser', password='testpass123')
        # Act
        response = self.client.post(reverse('add-books', kwargs={'list_id': self.user_list.id}), {
            'book_ids': [self.book.id],
        })
        # Assert
        self.assertRedirects(response, reverse('list-detail', kwargs={'list_id': self.user_list.id}))
        self.assertIn(self.book, self.user_list.books.all())

    
    def test_remove_book_from_list(self):
        # Arrange
        self.client.login(username='testuser', password='testpass123')
        self.user_list.books.add(self.book)
        # Act
        response = self.client.post(reverse('remove-books', kwargs={'list_id': self.user_list.id}), {
            'book_ids': [self.book.id],
        })
        # Assert
        self.assertRedirects(response, reverse('list-detail', kwargs={'list_id': self.user_list.id}))
        self.assertNotIn(self.book, self.user_list.books.all())


class ExportListTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.user_list = BookList.objects.create(user=self.user, name='My List')
        self.book = Book.objects.create(
            user=self.user,
            title='The Hobbit',
            author='J.R.R. Tolkien',
            status='finished',
            genre='fiction',
            rating=5,
        )
        self.user_list.books.add(self.book)

    def test_export_list_csv_returns_csv_file(self):
        # Arrange
        self.client.login(username='testuser', password='testpass123')
        # Act
        response = self.client.get(reverse('export-list', kwargs={'list_id': self.user_list.id, 'format': 'csv'}))
        # Assert - Check correct content type, book title is in file, and file is named correctly
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertIn('The Hobbit', response.content.decode())
        self.assertIn('my_list.csv', response['Content-Disposition'])

    def test_export_list_pdf_returns_pdf_file(self):
        # Arrange
        self.client.login(username='testuser', password='testpass123')
        # Act
        response = self.client.get(reverse('export-list', kwargs={'list_id': self.user_list.id, 'format': 'pdf'}))
        # Assert - Check correct content type and file is named correctly
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertIn('my_list.pdf', response['Content-Disposition'])


class ListDetailTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.user_list = BookList.objects.create(user=self.user, name='My List')
        self.book = Book.objects.create(
            user=self.user,
            title='The Hobbit',
            author='J.R.R. Tolkien',
            status='finished',
            genre='fiction',
        )
        self.user_list.books.add(self.book)

    
    def test_list_detail_shows_books_in_list(self):
        # Arrange
        self.client.login(username='testuser', password='testpass123')
        # Act
        response = self.client.get(reverse('list-detail', kwargs={'list_id': self.user_list.id}))
        # Assert - Check the page loads and the book in the list is visible
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'The Hobbit')


class EditListTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.user_list = BookList.objects.create(user=self.user, name='My List')

    
    def test_edit_list_renames_list_and_redirects(self):
        # Arrange
        self.client.login(username='testuser', password='testpass123')
        # Act
        response = self.client.post(reverse('edit-list', kwargs={'list_id': self.user_list.id}), {
            'name': 'My Renamed List',
        })
        # Assert - Check redirect happens and the list now has the new name in the database
        self.assertRedirects(response, reverse('list-detail', kwargs={'list_id': self.user_list.id}))
        self.assertTrue(BookList.objects.filter(name='My Renamed List', user=self.user).exists())


class EssentialListTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.finished_book = Book.objects.create(
            user=self.user,
            title='The Hobbit',
            author='J.R.R. Tolkien',
            status='finished',
            genre='fiction',
        )
        self.reading_book = Book.objects.create(
            user=self.user,
            title='Atomic Habits',
            author='James Clear',
            status='currently_reading',
            genre='nonfiction',
        )
        self.want_book = Book.objects.create(
            user=self.user,
            title='The Alchemist',
            author='Paulo Coelho',
            status='want_to_read',
            genre='fiction',
        )

    
    def test_finished_list_only_shows_finished_books(self):
        # Arrange
        self.client.login(username='testuser', password='testpass123')
        # Act
        response = self.client.get(reverse('finished-list'))
        # Assert - Check finished book is shown and other statuses are not
        self.assertContains(response, 'The Hobbit')
        self.assertNotContains(response, 'Atomic Habits')
        self.assertNotContains(response, 'The Alchemist')

    
    def test_currently_reading_list_only_shows_currently_reading_books(self):
        # Arrange
        self.client.login(username='testuser', password='testpass123')
        # Act
        response = self.client.get(reverse('currently-reading-list'))
        # Assert - Check currently reading book is shown and other statuses are not
        self.assertContains(response, 'Atomic Habits')
        self.assertNotContains(response, 'The Hobbit')
        self.assertNotContains(response, 'The Alchemist')

    
    def test_want_to_read_list_only_shows_want_to_read_books(self):
        # Arrange
        self.client.login(username='testuser', password='testpass123')
        # Act
        response = self.client.get(reverse('want-to-read-list'))
        # Assert - Check want to read book is shown and other statuses are not
        self.assertContains(response, 'The Alchemist')
        self.assertNotContains(response, 'The Hobbit')
        self.assertNotContains(response, 'Atomic Habits')
