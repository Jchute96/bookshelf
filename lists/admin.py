from django.contrib import admin
from .models import BookList

# Register your models here.

# Register BookList model so I can see it in admin panel
admin.site.register(BookList)

