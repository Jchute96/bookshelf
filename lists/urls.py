from django.urls import path
from . import views

urlpatterns = [
    path('my-lists/', views.my_lists, name='my-lists'),
    path('create-list/', views.create_list, name='create-list'),
]