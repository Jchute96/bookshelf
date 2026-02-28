import sys
from django.contrib.auth.signals import user_logged_in
from django.utils import timezone
from datetime import timedelta
from django.core.management import call_command

def check_demo_reset(sender, user, request, **kwargs):

    # Skip during tests
    if 'test' in sys.argv:
        return

    # Make sure current user is the demo user
    if user.username != 'demo':
        return

    from demo.models import DemoResetLog

    # Get or create the reset log (uses last_reset_at instead of user.last_login,
    # because Django updates user.last_login before this signal handler runs)
    log, _ = DemoResetLog.objects.get_or_create(pk=1)

    # Trigger a reset if the demo has never been reset, or it has been over 24 hours
    if log.last_reset_at is None or timezone.now() - log.last_reset_at > timedelta(hours=24):
        call_command('reset_demo')
        log.last_reset_at = timezone.now()
        log.save()

# Connect the receiver to the signal
user_logged_in.connect(check_demo_reset)