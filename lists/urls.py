from django.urls import path
from . import views

urlpatterns = [
    path('my-lists/', views.my_lists, name='my-lists'),
]