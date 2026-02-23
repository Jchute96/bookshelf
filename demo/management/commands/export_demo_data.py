from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from books.models import Book
from lists.models import BookList

# Create Django management command that inherits from BaseCommand
class Command(BaseCommand):
    help = 'Exports demo account data as Python seed code'

    def handle(self, *args, **kwargs):
        # Try to see if there is a demo user to use if not display error message to output
        try:
            demo_user = User.objects.get(username='demo')
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('No demo user found'))
            return

        books = Book.objects.filter(user=demo_user)
        lists = BookList.objects.filter(user=demo_user)

        self.stdout.write('\n# ===== DEMO BOOKS =====\n')
        self.stdout.write('DEMO_BOOKS = [\n')

        for book in books:
            # Get the Cloudinary URL if image exists, otherwise None
            image_url = book.image.url if book.image else None

        # repre gives us code representation of a value
            self.stdout.write(f'''    {{
        "title": {repr(book.title)},
        "author": {repr(book.author)},
        "genre": {repr(book.genre)},
        "status": {repr(book.status)},
        "rating": {repr(book.rating)},
        "review": {repr(book.review)},
        "date_finished": {repr(str(book.date_finished) if book.date_finished else None)},
        "purchase_link": {repr(book.purchase_link)},
        "image_url": {repr(image_url)},
    }},\n''')

        self.stdout.write(']\n\n')

        self.stdout.write('# ===== DEMO LISTS =====\n')
        self.stdout.write('DEMO_LISTS = [\n')

        for user_list in lists:
            # Get the titles of books in this list so we can recreate the relationship
            book_titles = list(user_list.books.values_list('title', flat=True))
            self.stdout.write(f'''    {{
        "name": {repr(user_list.name)},
        "books": {repr(book_titles)},
    }},\n''')

        self.stdout.write(']\n')

        self.stdout.write(self.style.SUCCESS('\nExport complete! Copy the output above into your seed file.'))