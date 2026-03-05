from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import timedelta

from .models import Homework, HomeworkMaterial, StudentHomeworkSubmission
from .serializers import (
    HomeworkSerializer, HomeworkMaterialSerializer,
    StudentHomeworkSubmissionSerializer, StudentHomeworkSubmissionUpdateSerializer
)
from apps.core.permissions import IsTeacher, IsStudent, IsAcademicOffice


class HomeworkViewSet(viewsets.ModelViewSet):
    """Homework viewset."""
    queryset = Homework.objects.select_related('subject', 'teacher', 'group')
    serializer_class = HomeworkSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['subject', 'teacher', 'group', 'status']
    ordering_fields = ['deadline', 'created_at']
    ordering = ['-deadline']
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsTeacher()]
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming homeworks."""
        today = timezone.now()
        homeworks = self.queryset.filter(
            deadline__gte=today,
            status='published'
        ).order_by('deadline')
        
        serializer = self.get_serializer(homeworks, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_group(self, request):
        """Get homeworks by group."""
        group_id = request.query_params.get('group_id')
        if not group_id:
            return Response(
                {'error': 'group_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        homeworks = self.queryset.filter(group_id=group_id)
        serializer = self.get_serializer(homeworks, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_subject(self, request):
        """Get homeworks by subject."""
        subject_id = request.query_params.get('subject_id')
        if not subject_id:
            return Response(
                {'error': 'subject_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        homeworks = self.queryset.filter(subject_id=subject_id)
        serializer = self.get_serializer(homeworks, many=True)
        return Response(serializer.data)


class HomeworkMaterialViewSet(viewsets.ModelViewSet):
    """Homework Material viewset."""
    queryset = HomeworkMaterial.objects.select_related('homework')
    serializer_class = HomeworkMaterialSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['homework']
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsTeacher()]


class StudentHomeworkSubmissionViewSet(viewsets.ModelViewSet):
    """Student Homework Submission viewset."""
    queryset = StudentHomeworkSubmission.objects.select_related('homework', 'student')
    serializer_class = StudentHomeworkSubmissionSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['homework', 'student', 'status']
    ordering_fields = ['submitted_at', 'created_at']
    ordering = ['-submitted_at']
    
    def get_serializer_class(self):
        if self.action in ['partial_update', 'update']:
            return StudentHomeworkSubmissionUpdateSerializer
        return StudentHomeworkSubmissionSerializer
    
    @action(detail=False, methods=['get'])
    def my_submissions(self, request):
        """Get current user's submissions."""
        if not hasattr(request.user, 'student_profile'):
            return Response(
                {'error': 'User is not a student'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        submissions = self.queryset.filter(student=request.user.student_profile)
        serializer = self.get_serializer(submissions, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def pending(self, request):
        """Get pending submissions for teacher."""
        if not hasattr(request.user, 'teacher_profile'):
            return Response(
                {'error': 'User is not a teacher'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        teacher = request.user.teacher_profile
        submissions = self.queryset.filter(
            homework__teacher=teacher,
            status__in=['submitted', 'missing']
        )
        serializer = self.get_serializer(submissions, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def overdue(self, request):
        """Get overdue submissions."""
        now = timezone.now()
        submissions = self.queryset.filter(
            homework__deadline__lt=now,
            status__in=['pending', 'submitted']
        )
        serializer = self.get_serializer(submissions, many=True)
        return Response(serializer.data)
    
    @action(detail='true', methods=['post'])
    def submit(self, request, pk=None):
        """Submit homework."""
        submission = self.get_object()
        
        if submission.status not in ['pending', 'submitted']:
            return Response(
                {'error': 'Cannot submit homework in this status'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = StudentHomeworkSubmissionSerializer(
            submission,
            data={
                'submission_text': request.data.get('submission_text', submission.submission_text),
                'submission_file': request.FILES.get('submission_file', submission.submission_file),
                'status': 'submitted',
                'submitted_at': timezone.now()
            },
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
