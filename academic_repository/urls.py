from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),    # Directs to Django's built-in master admin area
    path('', include('projects.urls')), # Securely hands off all other traffic to your projects app
]
