from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    # Field that has a one to one relationship with User model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Field for a users profile picture stored in media/profile_pics/
    image = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    # Display username when profile object is printed
    def __str__(self):
        return f"{self.user.username}'s profile"
