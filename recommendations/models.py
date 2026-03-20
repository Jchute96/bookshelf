from django.db import models
from django.contrib.auth.models import User

class Recommendation(models.Model):
    
    # Each recommendation belongs to one user
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Each recommendation needs to know book's title, author, and reason recommended
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    reason = models.TextField()
    
    # Cover image and purchase links are optional because they might not return from google books api search
    cover_link = models.URLField(max_length=800, null=True, blank=True)
    purchase_link = models.URLField(max_length=800, null=True, blank=True)
    
    # Set the timestamp when the record is first created
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    
    
    
