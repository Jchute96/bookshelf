from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Book(models.Model):
    GENRE_CHOICES = [
        ('fiction', 'Fiction'),
        ('nonfiction', 'Non-Fiction'),
        ('mystery', 'Mystery'),
        ('scifi', 'Science Fiction'),
        ('fantasy', 'Fantasy'),
        ('thriller', 'Thriller'),
        ('romance', 'Romance'),
        ('biography', 'Biography'),
        ('history', 'History'),
        ('selfhelp', 'Self-Help'),
    ]
    
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review = models.TextField()
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES)
    date_finished = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f'{self.title}'
    
    # Order by title
    class Meta:
        ordering = ['title']
    
    
    
    

