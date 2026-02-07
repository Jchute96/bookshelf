from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm

# Create your views here.

def register(request):
    # If user submits the registration form
    if request.method == 'POST':
        
        #  Create and fill customized form with the user entered data
        form = CustomUserCreationForm(request.POST)
        
        # Verify the user entered data is valid
        if form.is_valid():
            # Create new user in database and return user object
            user = form.save()
            # Log new user in
            login(request, user)
            # Redirect them to the books home page books/
            return redirect('home')
    #  If user has not submitted form
    else:
        # Display empty customized form
        form = CustomUserCreationForm()
        
    context = {'form': form}
        
    # Display registration page with form variable to be displayed
    return render(request, 'registration/register.html', context)
            
            

