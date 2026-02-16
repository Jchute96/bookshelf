from django.urls import path
from . import views

urlpatterns = [
    path('my-lists/', views.my_lists, name='my-lists'),
    path('create-list/', views.create_list, name='create-list'),
    # Passes number from URL to view as a parameter
    path('my-lists/<int:list_id>/', views.list_detail, name='list-detail'),
    path('my-lists/<int:list_id>/add-books/', views.add_books, name='add-books'),
    path('my-lists/<int:list_id>/remove-books/', views.remove_books, name='remove-books'),
]

