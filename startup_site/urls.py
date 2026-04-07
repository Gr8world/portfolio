"""
URL configuration for startup_site project.
"""

from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views

urlpatterns = [
    path("", include("core.urls")),
]

# Error handlers
handler404 = "core.views.handler404"
handler500 = "core.views.handler500"

# Serve media and static files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
