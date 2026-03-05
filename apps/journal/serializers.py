from rest_framework import serializers
from .models import Attendance, Grade, StudentGradeAverage
from apps.academics.serializers import LessonSerializer
from apps.accounts.serializers import StudentSerializer


class AttendanceSerializer(serializers.ModelSerializer):
    """Attendance serializer."""
    lesson_info = LessonSerializer(source='lesson', read_only=True)
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    
    class Meta:
        model = Attendance
        fields = [
            'id', 'lesson', 'lesson_info', 'student', 'student_name',
            'status', 'comment', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class GradeSerializer(serializers.ModelSerializer):
    """Grade serializer."""
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    teacher_name = serializers.CharField(source='teacher.user.get_full_name', read_only=True)
    
    class Meta:
        model = Grade
        fields = [
            'id', 'student', 'student_name', 'subject', 'subject_name',
            'teacher', 'teacher_name', 'value', 'grade_type', 'comment',
            'date', 'created_at', 'updated_at'
        ]
        read_only_fields = ['date', 'created_at', 'updated_at']


class StudentGradeAverageSerializer(serializers.ModelSerializer):
    """Student Grade Average serializer."""
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    
    class Meta:
        model = StudentGradeAverage
        fields = [
            'id', 'student', 'student_name', 'subject', 'subject_name',
            'average_grade', 'total_grades', 'last_updated'
        ]
        read_only_fields = ['average_grade', 'total_grades', 'last_updated']


class BulkAttendanceSerializer(serializers.Serializer):
    """Serializer for bulk attendance creation."""
    lesson_id = serializers.IntegerField()
    students_data = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField(),
            required=['student_id', 'status']
        )
    )


class AttendanceStatisticsSerializer(serializers.Serializer):
    """Serializer for attendance statistics."""
    total_lessons = serializers.IntegerField()
    present = serializers.IntegerField()
    absent = serializers.IntegerField()
    late = serializers.IntegerField()
    excused_absence = serializers.IntegerField()
    attendance_percentage = serializers.FloatField()
