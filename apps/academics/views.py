from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import datetime, timedelta

from .models import Subject, Group, Schedule, Lesson
from .serializers import (
    SubjectSerializer, GroupSerializer, ScheduleSerializer,
    LessonSerializer, LessonDetailSerializer
)
from apps.core.permissions import IsAcademicOffice, IsTeacher, IsStudent


class SubjectViewSet(viewsets.ReadOnlyModelViewSet):
    """Subject viewset."""
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['name']


class GroupViewSet(viewsets.ModelViewSet):
    """Group viewset."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['name', 'academic_year']
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsAcademicOffice()]


class ScheduleViewSet(viewsets.ModelViewSet):
    """Schedule viewset."""
    queryset = Schedule.objects.select_related('group', 'subject', 'teacher')
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['group', 'subject', 'teacher', 'weekday']
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsAcademicOffice()]
    
    @action(detail=False, methods=['get'])
    def by_group(self, request):
        """Get schedule by group."""
        group_id = request.query_params.get('group_id')
        if not group_id:
            return Response(
                {'error': 'group_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        schedules = self.queryset.filter(group_id=group_id).order_by('weekday', 'start_time')
        serializer = self.get_serializer(schedules, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_teacher(self, request):
        """Get schedule by teacher."""
        teacher_id = request.query_params.get('teacher_id')
        if not teacher_id:
            return Response(
                {'error': 'teacher_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        schedules = self.queryset.filter(teacher_id=teacher_id).order_by('weekday', 'start_time')
        serializer = self.get_serializer(schedules, many=True)
        return Response(serializer.data)


class LessonViewSet(viewsets.ModelViewSet):
    """Lesson viewset."""
    queryset = Lesson.objects.select_related('schedule__group', 'schedule__subject', 'schedule__teacher')
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['schedule__group', 'schedule__subject', 'schedule__teacher', 'date']
    ordering_fields = ['date']
    ordering = ['-date']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return LessonDetailSerializer
        return LessonSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsTeacher()]
    
    @action(detail=False, methods=['get'])
    def today(self, request):
        """Get today's lessons."""
        today = timezone.now().date()
        lessons = self.queryset.filter(date=today, is_cancelled=False).order_by('schedule__start_time')
        serializer = self.get_serializer(lessons, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_group(self, request):
        """Get lessons by group."""
        group_id = request.query_params.get('group_id')
        if not group_id:
            return Response(
                {'error': 'group_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        lessons = self.queryset.filter(schedule__group_id=group_id)
        serializer = self.get_serializer(lessons, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_teacher(self, request):
        """Get lessons by teacher."""
        teacher_id = request.query_params.get('teacher_id')
        if not teacher_id:
            return Response(
                {'error': 'teacher_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        lessons = self.queryset.filter(schedule__teacher_id=teacher_id)
        serializer = self.get_serializer(lessons, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming lessons."""
        days = int(request.query_params.get('days', 7))
        today = timezone.now().date()
        end_date = today + timedelta(days=days)
        
        lessons = self.queryset.filter(
            date__gte=today,
            date__lte=end_date,
            is_cancelled=False
        ).order_by('date', 'schedule__start_time')
        
        serializer = self.get_serializer(lessons, many=True)
        return Response(serializer.data)
