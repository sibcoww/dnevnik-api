from django.contrib import admin
from .models import Attendance, Grade, StudentGradeAverage


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'lesson', 'status', 'created_at']
    list_filter = ['status', 'created_at', 'lesson__date']
    search_fields = ['student__user__first_name', 'lesson__schedule__group__name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'teacher', 'value', 'grade_type', 'date']
    list_filter = ['grade_type', 'date', 'subject']
    search_fields = ['student__user__first_name', 'subject__name', 'teacher__user__first_name']
    readonly_fields = ['date', 'created_at', 'updated_at']


@admin.register(StudentGradeAverage)
class StudentGradeAverageAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'average_grade', 'total_grades']
    list_filter = ['subject']
    search_fields = ['student__user__first_name', 'subject__name']
    readonly_fields = ['last_updated']
