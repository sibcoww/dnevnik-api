from rest_framework import serializers
from .models import Subject, Group, Schedule, Lesson, TeacherSubject
from apps.accounts.serializers import TeacherSerializer, UserSerializer


class SubjectSerializer(serializers.ModelSerializer):
    """Subject serializer."""
    
    class Meta:
        model = Subject
        fields = ['id', 'name', 'description']


class GroupSerializer(serializers.ModelSerializer):
    """Group serializer."""
    
    class Meta:
        model = Group
        fields = ['id', 'name', 'academic_year', 'description', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class TeacherSubjectSerializer(serializers.ModelSerializer):
    """Teacher-Subject relationship serializer."""
    teacher_name = serializers.CharField(source='teacher.user.get_full_name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    
    class Meta:
        model = TeacherSubject
        fields = ['id', 'teacher', 'teacher_name', 'subject', 'subject_name']


class ScheduleSerializer(serializers.ModelSerializer):
    """Schedule serializer."""
    group_name = serializers.CharField(source='group.name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    teacher_name = serializers.CharField(source='teacher.user.get_full_name', read_only=True)
    weekday_display = serializers.CharField(source='get_weekday_display', read_only=True)
    
    class Meta:
        model = Schedule
        fields = [
            'id', 'group', 'group_name', 'subject', 'subject_name',
            'teacher', 'teacher_name', 'weekday', 'weekday_display',
            'start_time', 'end_time', 'room', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class LessonSerializer(serializers.ModelSerializer):
    """Lesson serializer."""
    schedule_info = ScheduleSerializer(source='schedule', read_only=True)
    
    class Meta:
        model = Lesson
        fields = [
            'id', 'schedule', 'schedule_info', 'date',
            'topic', 'notes', 'is_cancelled', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class LessonDetailSerializer(serializers.ModelSerializer):
    """Detailed lesson serializer with full schedule info."""
    schedule = ScheduleSerializer(read_only=True)
    
    class Meta:
        model = Lesson
        fields = [
            'id', 'schedule', 'date',
            'topic', 'notes', 'is_cancelled', 'created_at', 'updated_at'
        ]
