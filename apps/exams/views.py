from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import timedelta

from .models import Exam, ExamResult, ExamQuestion
from .serializers import (
    ExamSerializer, ExamResultSerializer,
    ExamResultUpdateSerializer, ExamQuestionSerializer
)
from apps.core.permissions import IsTeacher, IsStudent, IsAcademicOffice, IsDirector


class ExamViewSet(viewsets.ModelViewSet):
    """Exam viewset."""
    queryset = Exam.objects.select_related('subject', 'teacher', 'group')
    serializer_class = ExamSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['subject', 'teacher', 'group', 'status']
    ordering_fields = ['date']
    ordering = ['date']
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsTeacher()]
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming exams."""
        now = timezone.now()
        exams = self.queryset.filter(
            date__gte=now,
            status__in=['planned', 'in_progress']
        ).order_by('date')
        
        serializer = self.get_serializer(exams, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_group(self, request):
        """Get exams by group."""
        group_id = request.query_params.get('group_id')
        if not group_id:
            return Response(
                {'error': 'group_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        exams = self.queryset.filter(group_id=group_id)
        serializer = self.get_serializer(exams, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_subject(self, request):
        """Get exams by subject."""
        subject_id = request.query_params.get('subject_id')
        if not subject_id:
            return Response(
                {'error': 'subject_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        exams = self.queryset.filter(subject_id=subject_id)
        serializer = self.get_serializer(exams, many=True)
        return Response(serializer.data)
    
    @action(detail='true', methods=['post'])
    def start(self, request, pk=None):
        """Start exam."""
        exam = self.get_object()
        if exam.status != 'planned':
            return Response(
                {'error': 'Only planned exams can be started'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        exam.status = 'in_progress'
        exam.save()
        
        serializer = self.get_serializer(exam)
        return Response(serializer.data)
    
    @action(detail='true', methods=['post'])
    def complete(self, request, pk=None):
        """Complete exam."""
        exam = self.get_object()
        if exam.status != 'in_progress':
            return Response(
                {'error': 'Only in-progress exams can be completed'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        exam.status = 'completed'
        exam.save()
        
        serializer = self.get_serializer(exam)
        return Response(serializer.data)


class ExamResultViewSet(viewsets.ModelViewSet):
    """Exam Result viewset."""
    queryset = ExamResult.objects.select_related('exam', 'student')
    serializer_class = ExamResultSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['exam', 'student']
    ordering_fields = ['grade', 'created_at']
    ordering = ['-grade']
    
    def get_serializer_class(self):
        if self.action in ['partial_update', 'update']:
            return ExamResultUpdateSerializer
        return ExamResultSerializer
    
    @action(detail=False, methods=['get'])
    def my_results(self, request):
        """Get current user's exam results."""
        if not hasattr(request.user, 'student_profile'):
            return Response(
                {'error': 'User is not a student'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        results = self.queryset.filter(student=request.user.student_profile)
        serializer = self.get_serializer(results, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_exam(self, request):
        """Get results by exam."""
        exam_id = request.query_params.get('exam_id')
        if not exam_id:
            return Response(
                {'error': 'exam_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        results = self.queryset.filter(exam_id=exam_id).order_by('-grade')
        serializer = self.get_serializer(results, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get exam statistics."""
        exam_id = request.query_params.get('exam_id')
        if not exam_id:
            return Response(
                {'error': 'exam_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        results = self.queryset.filter(exam_id=exam_id)
        if not results.exists():
            return Response({
                'total_students': 0,
                'average_grade': 0,
                'min_grade': 0,
                'max_grade': 0,
            })
        
        grades = results.values_list('grade', flat=True)
        total = len(grades)
        average = sum(grades) / total if total > 0 else 0
        
        return Response({
            'total_students': total,
            'average_grade': round(average, 2),
            'min_grade': min(grades),
            'max_grade': max(grades),
        })


class ExamQuestionViewSet(viewsets.ModelViewSet):
    """Exam Question viewset."""
    queryset = ExamQuestion.objects.select_related('exam')
    serializer_class = ExamQuestionSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['exam']
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsTeacher()]
