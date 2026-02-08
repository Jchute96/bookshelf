from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, EditUsernameForm, EditEmailForm


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

@login_required
def profile(request):
    
    # Get the current user information
    user = request.user
    
    context = {'user': user}
    # Display profile page
    return render(request, 'accounts/profile.html', context)

@login_required
def edit_username(request):
    if request.method == 'POST':
        # Fill form with POST data and tell it which user to update
        form = EditUsernameForm(request.POST, instance=request.user)
        
        # Verify the form is valid
        if form.is_valid():
            # Update the user's username
            form.save()
            # Redirect user to their profile page
            return redirect('profile')
    
    else:
        # Display form to user to fill out
        form = EditUsernameForm(instance=request.user)
    
    context = {'form': form}
    return render(request, 'accounts/edit_username.html', context)
        
@login_required
def edit_email(request):
    if request.method == 'POST':
        # Fill form with POST data and tell it which user to update
        form = EditEmailForm(request.POST, instance=request.user)
        
        # Verify the form is valid
        if form.is_valid():
            # Update the user's email
            form.save()
            # Redirect user to their profile page
            return redirect('profile')
    
    else:
        # Display form to user to fill out
        form = EditEmailForm(instance=request.user)
    
    context = {'form': form}
    return render(request, 'accounts/edit_email.html', context)
     
        
    
    
    
            
            

