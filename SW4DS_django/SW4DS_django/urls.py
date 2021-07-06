"""
URL Configuration
"""

from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', include('kickstart.urls')),
]
