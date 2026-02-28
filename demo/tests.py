from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

class DemoTests(TestCase):
    
    def setUp(self):
        self.demo_user = User.objects.create_user(username='demo', password='testpass123!')
        self.client.login(username='demo', password='testpass123!')
        
    def test_demo_user_cannot_access_delete_account(self):
        # Act - Try to access the delete account page as demo user and use follow to follow the redirect to get the final pages response
        response = self.client.get(reverse('delete_account'), follow=True)
        # Assert - That profile features disabled message displayed and user redirected to home page
        self.assertRedirects(response, reverse('home'))
        self.assertContains(response, 'Profile features are disabled in demo mode.')
        
    
    def test_demo_user_cannot_access_edit_email(self):
         # Act
        response = self.client.get(reverse('edit_email'), follow=True)
        # Assert
        self.assertRedirects(response, reverse('home'))
        self.assertContains(response, 'Profile features are disabled in demo mode.')
        
    def test_demo_user_cannot_access_edit_username(self):
         # Act
        response = self.client.get(reverse('edit_username'), follow=True)
        # Assert
        self.assertRedirects(response, reverse('home'))
        self.assertContains(response, 'Profile features are disabled in demo mode.') 
        
    def test_demo_user_cannot_access_upload_profile_picture(self):
         # Act
        response = self.client.get(reverse('upload_profile_picture'), follow=True)
        # Assert
        self.assertRedirects(response, reverse('home'))
        self.assertContains(response, 'Profile features are disabled in demo mode.')
        
        
    
    

