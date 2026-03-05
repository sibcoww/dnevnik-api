from rest_framework import serializers
from .models import Exam, ExamResult, ExamQuestion


class ExamQuestionSerializer(serializers.ModelSerializer):
    """Exam Question serializer."""
    
    class Meta:
        model = ExamQuestion
        fields = ['id', 'question_text', 'question_type', 'points', 'order']


class ExamSerializer(serializers.ModelSerializer):
    """Exam serializer."""
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    teacher_name = serializers.CharField(source='teacher.user.get_full_name', read_only=True)
    group_name = serializers.CharField(source='group.name', read_only=True)
    questions = ExamQuestionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Exam
        fields = [
            'id', 'subject', 'subject_name', 'teacher', 'teacher_name',
            'group', 'group_name', 'date', 'duration_minutes', 'location',
            'description', 'status', 'questions', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class ExamResultSerializer(serializers.ModelSerializer):
    """Exam Result serializer."""
    exam_info = ExamSerializer(source='exam', read_only=True)
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    percentage = serializers.FloatField(read_only=True)
    
    class Meta:
        model = ExamResult
        fields = [
            'id', 'exam', 'exam_info', 'student', 'student_name',
            'grade', 'comment', 'points_earned', 'points_total',
            'percentage', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class ExamResultUpdateSerializer(serializers.ModelSerializer):
    """Exam Result update serializer (grading)."""
    
    class Meta:
        model = ExamResult
        fields = ['grade', 'comment', 'points_earned', 'points_total']
