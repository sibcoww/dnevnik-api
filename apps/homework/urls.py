from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    HomeworkViewSet, HomeworkMaterialViewSet,
    StudentHomeworkSubmissionViewSet
)

app_name = 'homework'

router = DefaultRouter()
router.register(r'homeworks', HomeworkViewSet, basename='homework')
router.register(r'materials', HomeworkMaterialViewSet, basename='material')
router.register(r'submissions', StudentHomeworkSubmissionViewSet, basename='submission')

urlpatterns = [
    path('', include(router.urls)),
]
