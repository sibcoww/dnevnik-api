from django.db import models
from apps.core.models import TimeStampedModel
from apps.accounts.models import Teacher, Student
from apps.academics.models import Subject, Group


class Exam(TimeStampedModel):
    """Exam model."""
    
    STATUS_CHOICES = (
        ('planned', 'Planned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='exams')
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT, related_name='exams_supervised')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='exams')
    date = models.DateTimeField()
    duration_minutes = models.IntegerField(default=60)
    location = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    
    class Meta:
        verbose_name = 'Exam'
        verbose_name_plural = 'Exams'
        ordering = ['date']
    
    def __str__(self):
        return f'{self.subject} - {self.group} ({self.date})'


class ExamResult(TimeStampedModel):
    """Exam Result model."""
    
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='results')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='exam_results')
    grade = models.IntegerField()
    comment = models.TextField(blank=True)
    points_earned = models.IntegerField(null=True, blank=True)
    points_total = models.IntegerField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Exam Result'
        verbose_name_plural = 'Exam Results'
        unique_together = ['exam', 'student']
        ordering = ['-grade']
    
    def __str__(self):
        return f'{self.student} - {self.exam}: {self.grade}'
    
    @property
    def percentage(self):
        if self.points_total and self.points_total > 0:
            return round((self.points_earned / self.points_total) * 100, 2)
        return None


class ExamQuestion(TimeStampedModel):
    """Exam Question (optional for quiz system)."""
    
    QUESTION_TYPES = (
        ('multiple_choice', 'Multiple Choice'),
        ('short_answer', 'Short Answer'),
        ('essay', 'Essay'),
        ('true_false', 'True/False'),
    )
    
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    points = models.IntegerField(default=1)
    order = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = 'Exam Question'
        verbose_name_plural = 'Exam Questions'
        ordering = ['order']
    
    def __str__(self):
        return f'{self.exam} - Question {self.order}'
