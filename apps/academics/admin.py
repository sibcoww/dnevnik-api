from django.contrib import admin
from .models import Subject, Group, Schedule, Lesson, TeacherSubject


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'academic_year', 'created_at']
    list_filter = ['academic_year', 'created_at']
    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['group', 'subject', 'teacher', 'get_weekday_display', 'start_time', 'end_time']
    list_filter = ['weekday', 'group', 'subject']
    search_fields = ['group__name', 'subject__name', 'teacher__user__first_name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['schedule', 'date', 'topic', 'is_cancelled']
    list_filter = ['date', 'is_cancelled', 'schedule__group']
    search_fields = ['schedule__group__name', 'schedule__subject__name', 'topic']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(TeacherSubject)
class TeacherSubjectAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'subject']
    list_filter = ['subject']
    search_fields = ['teacher__user__first_name', 'subject__name']
