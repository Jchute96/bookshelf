from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, EditUsernameForm, EditEmailForm, DeleteAccountForm, ProfilePictureForm
from .models import Profile
from demo.decorators import demo_restricted


# Create your views here.

# Registration page
def register(request):
    
    #  Redirect to home if user is already logged in
    if request.user.is_authenticated:
        return redirect('home')
    
    # If user submits the registration form
    if request.method == 'POST':
        
        #  Create and fill customized form with the user entered data
        form = CustomUserCreationForm(request.POST)
        
        # Verify the user entered data is valid
        if form.is_valid():
            # Create new user in database and return user object
            user = form.save()
            # Create a profile for the new user
            Profile.objects.create(user=user)
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
@demo_restricted
def profile(request):
    
    # Get the current user information
    user = request.user
    
    context = {'user': user}
    # Display profile page
    return render(request, 'accounts/profile.html', context)

@login_required
@demo_restricted
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
@demo_restricted
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

# Account deletion page
@login_required
@demo_restricted
def delete_account(request):
    if request.method == 'POST':
        form = DeleteAccountForm(request.POST)
        
        if form.is_valid():
            # Get the password from the form and validate and clean the user input
            password = form.cleaned_data['password']
            
            # If password entered matches the active users password
            if request.user.check_password(password):
                # Delete current user
                request.user.delete()
                # Redirect to registration page
                return redirect('account_deleted')
            else:
                # Display error message if passwords do not match
                form.add_error('password', 'Incorrect password. Please try again.')
    
    # Display form  
    else:
        form = DeleteAccountForm()
            
    context = {'form': form}
    return render(request, 'accounts/delete_account.html', context)
                
# Confirmation of account deletion for user
def account_deleted(request):
    return render(request, 'accounts/account_deleted.html')            
                
# Upload a profile picture
@login_required
@demo_restricted
def upload_profile_picture(request):
    if request.method == 'POST':
        # Fill form with file from the POST data and tell it which users profile to update
        # instance= tells us to update the current instance instead of creating a new one
        form = ProfilePictureForm(request.POST, request.FILES, instance=request.user.profile)
        
        if form.is_valid():
            form.save()
            return redirect('profile')
        
    else:
        form = ProfilePictureForm(instance=request.user.profile)
    
    context = {'form': form}
    
    return render(request, 'accounts/upload_profile_picture.html', context)
        
            
    
        
            
            
