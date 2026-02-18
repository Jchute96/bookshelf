# Imports user model for user profiles
from django.contrib.auth.models import User
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
    
    STATUS_CHOICES = [
        ('want_to_read', 'Want to Read'),
        ('currently_reading', 'Currently Reading'),
        ('finished', 'Finished'),
    ]
    
    # When user deletes profile delete all of the data associated with their foreign key
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='finished')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True)
    review = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES)
    date_finished = models.DateField(null=True, blank=True)
    purchase_link = models.URLField(max_length=800, null=True, blank=True)
    
    def __str__(self):
        return f'{self.title}'
    
    # Order by title
    class Meta:
        ordering = ['title']
        
    # Method that returns total stars filled/unfilled corresponding to the book rating
    def get_star_display(self):
        if self.rating is None:
            return ''
        
        filled_stars = '⭐' * self.rating
        empty_stars = '☆' * (5 - self.rating)
        
        stars = filled_stars + empty_stars
        
        return stars
        
        
    
    
    
    

