from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('book-detail/<uuid:id>/', views.book_detail, name='book-detail'),
    path('add-book/', views.add_book, name='add-book'),
    path('edit-book/<uuid:id>/', views.edit_book, name='edit-book'),
    path('delete-book/<uuid:id>/', views.delete_book, name='delete-book'),
    path('statistics/', views.statistics, name='statistics'),
    path('api/search-google-books/', views.search_google_books, name='search-google-books'),
]