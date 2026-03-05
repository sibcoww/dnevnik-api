from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

app_name = 'sysadmin'

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='admin-user')

urlpatterns = [
    path('', include(router.urls)),
]
