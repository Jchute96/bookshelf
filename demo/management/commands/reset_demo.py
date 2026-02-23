from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from books.models import Book
from lists.models import BookList
from demo.seed_data import DEMO_BOOKS, DEMO_LISTS

class Command(BaseCommand):
    help = 'Resets the demo account to its original seed data'
    
    def get_image_path(self, image_url):
        # If no image, return None
        if not image_url:
            return None
        
        # Split on '/media/' and take everything after it
        # e.g. 'https://.../media/images/1984_xi9gf3' → 'images/1984_xi9gf3'
        if '/media/' in image_url:
            return image_url.split('/media/')[1]
        return image_url

    def handle(self, *args, **kwargs):
        # Get the demo user
        try:
            demo_user = User.objects.get(username='demo')
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('No demo user found'))
            return

        # Delete all existing books and lists for demo user
        # Deleting books will also clean up any list relationships automatically
        Book.objects.filter(user=demo_user).delete()
        BookList.objects.filter(user=demo_user).delete()
        self.stdout.write('Deleted existing demo data')

        # Recreate all books from seed data
        for book_data in DEMO_BOOKS:
            Book.objects.create(
                user=demo_user,
                title=book_data['title'],
                author=book_data['author'],
                genre=book_data['genre'],
                status=book_data['status'],
                rating=book_data['rating'],
                review=book_data['review'],
                date_finished=book_data['date_finished'],
                purchase_link=book_data['purchase_link'],
                image=self.get_image_path(book_data['image_url']),
            )
        self.stdout.write(f'Created {len(DEMO_BOOKS)} books')

        # Recreate all lists and reconnect books by title
        for list_data in DEMO_LISTS:
            new_list = BookList.objects.create(
                user=demo_user,
                name=list_data['name']
            )
            # Look up each book by title and add it to the list
            for title in list_data['books']:
                try:
                    book = Book.objects.get(title=title, user=demo_user)
                    new_list.books.add(book)
                except Book.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f'Book not found: {title}'))

        self.stdout.write(f'Created {len(DEMO_LISTS)} lists')
        self.stdout.write(self.style.SUCCESS('Demo account reset successfully!'))