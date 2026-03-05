from django.db import models
from apps.core.models import TimeStampedModel
from apps.accounts.models import User, Teacher


class Subject(models.Model):
    """Subject model."""
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Group(models.Model):
    """Group/Class model."""
    name = models.CharField(max_length=50, unique=True)
    academic_year = models.CharField(max_length=10)  # e.g., "2024-2025"
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'
        ordering = ['academic_year', 'name']
    
    def __str__(self):
        return f'{self.name} ({self.academic_year})'


class TeacherSubject(models.Model):
    """Relationship between teachers and subjects."""
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='subjects')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='teachers')
    
    class Meta:
        unique_together = ['teacher', 'subject']
        verbose_name = 'Teacher Subject'
        verbose_name_plural = 'Teacher Subjects'
    
    def __str__(self):
        return f'{self.teacher} - {self.subject}'


class Schedule(TimeStampedModel):
    """Class schedule model."""
    
    WEEKDAY_CHOICES = (
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    )
    
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='schedules')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='schedules')
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT, related_name='schedules')
    weekday = models.IntegerField(choices=WEEKDAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=50, blank=True)
    
    class Meta:
        verbose_name = 'Schedule'
        verbose_name_plural = 'Schedules'
        unique_together = ['group', 'subject', 'weekday', 'start_time']
        ordering = ['group', 'weekday', 'start_time']
    
    def __str__(self):
        return f'{self.group} - {self.subject} ({self.get_weekday_display()})'


class Lesson(TimeStampedModel):
    """Lesson model."""
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='lessons')
    date = models.DateField()
    topic = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    is_cancelled = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Lesson'
        verbose_name_plural = 'Lessons'
        unique_together = ['schedule', 'date']
        ordering = ['-date']
    
    def __str__(self):
        return f'{self.schedule.group} - {self.schedule.subject} ({self.date})'
