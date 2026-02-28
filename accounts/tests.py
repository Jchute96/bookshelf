from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Profile

# Create your tests here.

class RegistrationTests(TestCase):
    
    def setUp(self):
        # Create a user to test duplicate username
        self.existing_user = User.objects.create_user(username='existinguser', password='testpass123!')
    
    def test_new_registered_user_exists_in_database(self):
        # Act - Submit a post request with the registration form data
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password1': 'testpass123!',
            'password2': 'testpass123!',
        })
        # Assert - Verify user who just registered is in the database and they are redirected to home page
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertRedirects(response, reverse('home'))
        
    def test_profile_created_for_newly_registered_user(self):
        # Act
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password1': 'testpass123!',
            'password2': 'testpass123!',
        })
        
        # Assert
        user = User.objects.get(username='newuser')
        self.assertTrue(Profile.objects.filter(user=user).exists())
        
    def test_user_logged_in_after_registration(self):
        # Act
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password1': 'testpass123!',
            'password2': 'testpass123!',
        })
        
        # Assert - Check if new user is logged in after post request
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        
    def test_duplicate_usernames_not_created(self):
        # Act
        response = self.client.post(reverse('register'), {
            'username': 'existinguser',
            'email': 'existinguser@test.com',
            'password1': 'testpass123!',
            'password2': 'testpass123!',
        })
        
        # Assert - Make sure error message displays and that there is only one user with that username that exists
        self.assertContains(response, 'A user with that username already exists.')
        self.assertEqual(User.objects.filter(username='existinguser').count(), 1)
        
        
       
    
