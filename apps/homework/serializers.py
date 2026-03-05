from rest_framework import serializers
from .models import Homework, HomeworkMaterial, StudentHomeworkSubmission


class HomeworkMaterialSerializer(serializers.ModelSerializer):
    """Homework Material serializer."""
    
    class Meta:
        model = HomeworkMaterial
        fields = ['id', 'title', 'description', 'file', 'link', 'created_at']
        read_only_fields = ['created_at']


class HomeworkSerializer(serializers.ModelSerializer):
    """Homework serializer."""
    materials = HomeworkMaterialSerializer(many=True, read_only=True)
    teacher_name = serializers.CharField(source='teacher.user.get_full_name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    group_name = serializers.CharField(source='group.name', read_only=True)
    
    class Meta:
        model = Homework
        fields = [
            'id', 'subject', 'subject_name', 'teacher', 'teacher_name',
            'group', 'group_name', 'title', 'description', 'deadline',
            'status', 'materials', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class StudentHomeworkSubmissionSerializer(serializers.ModelSerializer):
    """Student Homework Submission serializer."""
    homework_info = HomeworkSerializer(source='homework', read_only=True)
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    
    class Meta:
        model = StudentHomeworkSubmission
        fields = [
            'id', 'homework', 'homework_info', 'student', 'student_name',
            'submission_text', 'submission_file', 'submitted_at', 'grade',
            'feedback', 'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['submitted_at', 'created_at', 'updated_at']


class StudentHomeworkSubmissionUpdateSerializer(serializers.ModelSerializer):
    """Student Homework Submission update serializer (grading)."""
    
    class Meta:
        model = StudentHomeworkSubmission
        fields = ['grade', 'feedback', 'status']
