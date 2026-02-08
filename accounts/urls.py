from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('edit-username/', views.edit_username, name='edit_username'),
    path('edit-email/', views.edit_email, name='edit_email'),
]