from django.db.models.signals import post_save
from django.dispatch import receiver
from books.models import Book
from .models import Recommendation

# Listen for when a book is saved
@receiver(post_save, sender=Book)


def reset_recommendations(sender, instance, **kwargs):
    
    # Delete all recommendations for the user given by the book instance just added
    Recommendation.objects.filter(user=instance.user).delete()