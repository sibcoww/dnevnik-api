from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Count, Avg, F
from django.utils import timezone

from .models import Attendance, Grade, StudentGradeAverage
from .serializers import (
    AttendanceSerializer, GradeSerializer,
    StudentGradeAverageSerializer, BulkAttendanceSerializer,
    AttendanceStatisticsSerializer
)
from apps.core.permissions import IsTeacher, IsStudent, IsAcademicOffice, IsDirector
from apps.accounts.models import Student


class AttendanceViewSet(viewsets.ModelViewSet):
    """Attendance viewset."""
    queryset = Attendance.objects.select_related('lesson', 'student', 'student__user')
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['lesson', 'student', 'status']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsTeacher()]
    
    def create(self, request, *args, **kwargs):
        """Create attendance record."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        """Bulk create attendance records."""
        serializer = BulkAttendanceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        lesson_id = serializer.validated_data['lesson_id']
        students_data = serializer.validated_data['students_data']
        
        attendances = []
        for student_data in students_data:
            attendance = Attendance(
                lesson_id=lesson_id,
                student_id=student_data['student_id'],
                status=student_data['status'],
                comment=student_data.get('comment', '')
            )
            attendances.append(attendance)
        
        Attendance.objects.bulk_create(attendances, ignore_conflicts=True)
        return Response(
            {'message': f'{len(attendances)} attendance records created.'},
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=False, methods=['get'])
    def by_student(self, request):
        """Get attendance by student."""
        student_id = request.query_params.get('student_id')
        if not student_id:
            return Response(
                {'error': 'student_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        attendances = self.queryset.filter(student_id=student_id)
        serializer = self.get_serializer(attendances, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get attendance statistics for a student."""
        student_id = request.query_params.get('student_id')
        if not student_id:
            return Response(
                {'error': 'student_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        attendances = self.queryset.filter(student_id=student_id)
        total = attendances.count()
        
        if total == 0:
            return Response({
                'total_lessons': 0,
                'present': 0,
                'absent': 0,
                'late': 0,
                'excused_absence': 0,
                'attendance_percentage': 0,
            })
        
        stats = {
            'total_lessons': total,
            'present': attendances.filter(status='present').count(),
            'absent': attendances.filter(status='absent').count(),
            'late': attendances.filter(status='late').count(),
            'excused_absence': attendances.filter(status='excused_absence').count(),
        }
        
        present_count = stats['present'] + stats['late']
        stats['attendance_percentage'] = round((present_count / total) * 100, 2)
        
        return Response(stats)


class GradeViewSet(viewsets.ModelViewSet):
    """Grade viewset."""
    queryset = Grade.objects.select_related('student', 'subject', 'teacher')
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['student', 'subject', 'teacher', 'grade_type', 'date']
    ordering_fields = ['date', 'value']
    ordering = ['-date']
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsTeacher()]
    
    @action(detail=False, methods=['get'])
    def by_student(self, request):
        """Get grades by student."""
        student_id = request.query_params.get('student_id')
        if not student_id:
            return Response(
                {'error': 'student_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        grades = self.queryset.filter(student_id=student_id)
        serializer = self.get_serializer(grades, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_subject(self, request):
        """Get grades by subject."""
        subject_id = request.query_params.get('subject_id')
        if not subject_id:
            return Response(
                {'error': 'subject_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        grades = self.queryset.filter(subject_id=subject_id)
        serializer = self.get_serializer(grades, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def average_by_student_subject(self, request):
        """Get average grade by student and subject."""
        student_id = request.query_params.get('student_id')
        subject_id = request.query_params.get('subject_id')
        
        if not student_id or not subject_id:
            return Response(
                {'error': 'Both student_id and subject_id are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        grades = self.queryset.filter(
            student_id=student_id,
            subject_id=subject_id
        ).values_list('value', flat=True)
        
        if not grades:
            return Response({
                'student_id': student_id,
                'subject_id': subject_id,
                'average': 0,
                'count': 0,
            })
        
        avg = sum(grades) / len(grades)
        return Response({
            'student_id': student_id,
            'subject_id': subject_id,
            'average': round(avg, 2),
            'count': len(grades),
        })


class StudentGradeAverageViewSet(viewsets.ReadOnlyModelViewSet):
    """Student Grade Average viewset."""
    queryset = StudentGradeAverage.objects.select_related('student', 'subject')
    serializer_class = StudentGradeAverageSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['student', 'subject']
