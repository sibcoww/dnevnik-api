"""
URL configuration for dnevnik_project.
"""

from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # API v1
    path('api/v1/auth/', include('apps.accounts.urls', namespace='auth')),
    path('api/v1/academics/', include('apps.academics.urls', namespace='academics')),
    path('api/v1/journal/', include('apps.journal.urls', namespace='journal')),
    path('api/v1/homework/', include('apps.homework.urls', namespace='homework')),
    path('api/v1/exams/', include('apps.exams.urls', namespace='exams')),
    path('api/v1/sysadmin/', include('apps.accounts.admin_urls', namespace='sysadmin')),
]
