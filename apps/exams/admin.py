from django.contrib import admin
from .models import Exam, ExamResult, ExamQuestion


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['subject', 'group', 'date', 'teacher', 'status']
    list_filter = ['status', 'date', 'subject', 'group']
    search_fields = ['subject__name', 'group__name', 'teacher__user__first_name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):
    list_display = ['student', 'exam', 'grade', 'percentage']
    list_filter = ['exam', 'grade']
    search_fields = ['student__user__first_name', 'exam__subject__name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ExamQuestion)
class ExamQuestionAdmin(admin.ModelAdmin):
    list_display = ['exam', 'question_text', 'question_type', 'points', 'order']
    list_filter = ['question_type', 'exam']
    search_fields = ['exam__subject__name', 'question_text']
    readonly_fields = ['created_at', 'updated_at']
