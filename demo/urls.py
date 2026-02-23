from django.urls import path
from . import views

urlpatterns = [
    path('demo-login/', views.demo_login, name='demo-login')
]