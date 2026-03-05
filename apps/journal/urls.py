from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AttendanceViewSet, GradeViewSet, StudentGradeAverageViewSet

app_name = 'journal'

router = DefaultRouter()
router.register(r'attendance', AttendanceViewSet, basename='attendance')
router.register(r'grades', GradeViewSet, basename='grade')
router.register(r'grade-averages', StudentGradeAverageViewSet, basename='grade-average')

urlpatterns = [
    path('', include(router.urls)),
]
