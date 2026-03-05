from django.contrib import admin
from .models import Homework, HomeworkMaterial, StudentHomeworkSubmission


@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'teacher', 'group', 'deadline', 'status']
    list_filter = ['status', 'deadline', 'subject', 'group']
    search_fields = ['title', 'subject__name', 'teacher__user__first_name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(HomeworkMaterial)
class HomeworkMaterialAdmin(admin.ModelAdmin):
    list_display = ['homework', 'title', 'file', 'link']
    list_filter = ['created_at']
    search_fields = ['homework__title', 'title']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(StudentHomeworkSubmission)
class StudentHomeworkSubmissionAdmin(admin.ModelAdmin):
    list_display = ['student', 'homework', 'status', 'submitted_at', 'grade']
    list_filter = ['status', 'submitted_at', 'homework']
    search_fields = ['student__user__first_name', 'homework__title']
    readonly_fields = ['created_at', 'updated_at']
