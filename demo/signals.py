from django.contrib.auth.signals import user_logged_in
from django.utils import timezone
from datetime import timedelta
from django.core.management import call_command

def check_demo_reset(sender, user, request, **kwargs):
    
    # Make sure current user is the demo user
    if user.username != 'demo':
        return
    
    # Verify it has been over 24 hours since last time a demo user logged in
    if user.last_login and timezone.now() - user.last_login > timedelta(hours=24):
        
        # Trigger the reset demo management command by using call_command
        call_command('reset_demo')

# Connect the receiver to the signal
user_logged_in.connect(check_demo_reset)