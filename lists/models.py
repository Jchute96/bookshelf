from django.db import models
from django.contrib.auth.models import User
from books.models import Book
import uuid


class BookList(models.Model):
    
    # Create Universally unique indetifier field that generates a default uuid that is unique and can not be edited
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    # Each list belongs to one user
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Name of list
    name = models.CharField(max_length=100)
    # A list can have many books and one book can belong to many lists
    books = models.ManyToManyField(Book, blank=True)
    # Get date when list is created
    created_date = models.DateTimeField(auto_now_add=True)
    
    # Display list name when list object printed
    def __str__(self):
        return self.name
    
    # Display newly created lists first
    class Meta:
        ordering = ['-created_date']
    
    
    
    
