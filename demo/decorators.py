from django.contrib import messages
from django.shortcuts import redirect
from functools import wraps

# Decorator to restrict demo account from accessing certain views
def demo_restricted(view_func):
    # Make sure wraps preserves the original function's name and docsrting
    @wraps(view_func)
    
    # Function that runs when someone visits url with this decorator
    # args and kwargs handles any url parameters
    def wrapper(request, *args, **kwargs):
        # Check if current user is the demo user
        if request.user.username == 'demo':
            # Add a warning message that will display on the next page and return demo user to home page
            messages.warning(request, 'This feature is disabled in demo mode.')
            return redirect('home')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper