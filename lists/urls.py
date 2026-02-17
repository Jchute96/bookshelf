from django.urls import path
from . import views

urlpatterns = [
    path('my-lists/', views.my_lists, name='my-lists'),
    path('create-list/', views.create_list, name='create-list'),
    path('my-lists/finished/', views.essential_list, {'status': 'finished'}, name='finished-list'),
    path('my-lists/currently-reading/', views.essential_list, {'status': 'currently_reading'}, name='currently-reading-list'),
    path('my-lists/want-to-read/', views.essential_list, {'status': 'want_to_read'}, name='want-to-read-list'),
    path('my-lists/finished/export/<str:format>/', views.export_list, {'status': 'finished'},  name='export-finished'),
    path('my-lists/currently-reading/export/<str:format>/', views.export_list, {'status': 'currently_reading'}, name='export-currently-reading'),
    path('my-lists/want-to-read/export/<str:format>/', views.export_list, {'status': 'want_to_read'}, name='export-want-to-read'),
    # Passes number from URL to view as a parameter
    path('my-lists/<int:list_id>/', views.list_detail, name='list-detail'),
    path('my-lists/<int:list_id>/add-books/', views.add_books, name='add-books'),
    path('my-lists/<int:list_id>/remove-books/', views.remove_books, name='remove-books'),
    path('my-lists/<int:list_id>/edit/', views.edit_list, name='edit-list'),
    path('my-lists/<int:list_id>/delete/', views.delete_list, name='delete-list'),
    path('my-lists/<int:list_id>/export/<str:format>/', views.export_list, name='export-list'),
    
]

