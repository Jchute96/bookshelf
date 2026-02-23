from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib.auth.models import User

# Create your views here.

def demo_login(request):
    try:
        # Get the demo user
        demo_user = User.objects.get(username='demo')
        
        # Log the demo user in without needing to provide credentials to user
        # Use backend= to identify which backend authentication to use
        login(request, demo_user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('home')
    
    except User.DoesNotExist:
        return redirect('login')
    
    