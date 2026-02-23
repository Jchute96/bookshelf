"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from demo.decorators import demo_restricted

urlpatterns = [
    # Override the login URL to redirect authenticated users
    path('accounts/login/', auth_views.LoginView.as_view(redirect_authenticated_user=True)),
    # Wrap Django's built in password change view with demo_restricted so demo users can not access it
    path('accounts/password_change/', demo_restricted(auth_views.PasswordChangeView.as_view()), name='password_change'),
    path('admin/', admin.site.urls),
    #  Direct any urls starting with /accounts/ and that are in Django's pre built authentication URLs
    path('accounts/', include('django.contrib.auth.urls')),
    #  Direct any urls starting with /accounts/ to the custom accounts URLs
    path('accounts/', include('accounts.urls')),
    path('books/', include('books.urls')),
    path('lists/', include('lists.urls')),
    path('', include('demo.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
