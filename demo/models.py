from django.db import models


# Create new model to track the last time demo user was reset
class DemoResetLog(models.Model):
    last_reset_at = models.DateTimeField(null=True, blank=True)
