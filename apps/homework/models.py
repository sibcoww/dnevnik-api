from django.db import models
from django.core.validators import FileExtensionValidator
from apps.core.models import TimeStampedModel
from apps.accounts.models import Teacher
from apps.academics.models import Subject, Group


class Homework(TimeStampedModel):
    """Homework model."""
    
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('closed', 'Closed'),
    )
    
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='homeworks')
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT, related_name='homeworks_created')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='homeworks')
    title = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    class Meta:
        verbose_name = 'Homework'
        verbose_name_plural = 'Homeworks'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.title} - {self.group} ({self.subject})'


class HomeworkMaterial(TimeStampedModel):
    """Homework Materials (files and links)."""
    
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, related_name='materials')
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    file = models.FileField(
        upload_to='homework/materials/%Y/%m/',
        blank=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'txt', 'jpg', 'png', 'zip']
            )
        ]
    )
    link = models.URLField(blank=True)
    
    class Meta:
        verbose_name = 'Homework Material'
        verbose_name_plural = 'Homework Materials'
        ordering = ['created_at']
    
    def __str__(self):
        return f'{self.homework} - {self.title or self.file.name or self.link}'


class StudentHomeworkSubmission(TimeStampedModel):
    """Student homework submission."""
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('submitted', 'Submitted'),
        ('graded', 'Graded'),
        ('missing', 'Missing'),
    )
    
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey('accounts.Student', on_delete=models.CASCADE, related_name='homework_submissions')
    submission_text = models.TextField(blank=True)
    submission_file = models.FileField(upload_to='homework/submissions/%Y/%m/', blank=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    grade = models.IntegerField(null=True, blank=True)
    feedback = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    class Meta:
        verbose_name = 'Student Homework Submission'
        verbose_name_plural = 'Student Homework Submissions'
        unique_together = ['homework', 'student']
        ordering = ['-submitted_at']
    
    def __str__(self):
        return f'{self.student} - {self.homework}'
