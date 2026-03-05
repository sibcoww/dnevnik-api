from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubjectViewSet, GroupViewSet, ScheduleViewSet, LessonViewSet

app_name = 'academics'

router = DefaultRouter()
router.register(r'subjects', SubjectViewSet, basename='subject')
router.register(r'groups', GroupViewSet, basename='group')
router.register(r'schedules', ScheduleViewSet, basename='schedule')
router.register(r'lessons', LessonViewSet, basename='lesson')

urlpatterns = [
    path('', include(router.urls)),
]
