from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExamViewSet, ExamResultViewSet, ExamQuestionViewSet

app_name = 'exams'

router = DefaultRouter()
router.register(r'exams', ExamViewSet, basename='exam')
router.register(r'results', ExamResultViewSet, basename='result')
router.register(r'questions', ExamQuestionViewSet, basename='question')

urlpatterns = [
    path('', include(router.urls)),
]
