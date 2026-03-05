from django.db import models
from apps.core.models import TimeStampedModel
from apps.accounts.models import Student, Teacher
from apps.academics.models import Lesson, Subject


class Attendance(TimeStampedModel):
    """Attendance model."""
    
    STATUS_CHOICES = (
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused_absence', 'Excused Absence'),
    )
    
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='attendances')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='present')
    comment = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendances'
        unique_together = ['lesson', 'student']
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.student} - {self.lesson} ({self.status})'


class Grade(TimeStampedModel):
    """Grade model."""
    
    GRADE_TYPES = (
        ('homework', 'Homework'),
        ('classwork', 'Classwork'),
        ('test', 'Test'),
        ('exam', 'Exam'),
        ('project', 'Project'),
        ('quiz', 'Quiz'),
    )
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='grades')
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT, related_name='grades_given')
    value = models.IntegerField()  # 1-5 scale or other grading system
    grade_type = models.CharField(max_length=20, choices=GRADE_TYPES)
    comment = models.TextField(blank=True)
    date = models.DateField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Grade'
        verbose_name_plural = 'Grades'
        ordering = ['-date']
    
    def __str__(self):
        return f'{self.student} - {self.subject}: {self.value}'


class StudentGradeAverage(models.Model):
    """Cached average grades for students."""
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='grade_average')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    average_grade = models.FloatField()
    total_grades = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['student', 'subject']
        verbose_name = 'Student Grade Average'
        verbose_name_plural = 'Student Grade Averages'
    
    def __str__(self):
        return f'{self.student} - {self.subject}: {self.average_grade}'
