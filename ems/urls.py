# ems/urls.py

from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({"status": "healthy"})

urlpatterns = [
    # Django admin site
    path('admin/', admin.site.urls),
    
    # Include URLs from the 'core' app
    path('', include('core.urls')),
    
    # Health check endpoint
    path('health/', health_check, name='health_check'),
]
