from django.urls import path
from . import views

urlpatterns = [
    path('my-recommendations/', views.my_recommendations, name='my-recommendations'),
]