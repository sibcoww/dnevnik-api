"""
Django management command for creating test data.

Usage:
    python manage.py shell < create_test_data.py
"""

from django.utils import timezone
from datetime import timedelta
from apps.accounts.models import User, Teacher, Student
from apps.academics.models import Subject, Group, Schedule, Lesson, TeacherSubject
from apps.journal.models import Attendance, Grade
from apps.homework.models import Homework, HomeworkMaterial
from apps.exams.models import Exam, ExamResult

# Очистить существующие данные (опционально)
# User.objects.filter(role__in=['student', 'teacher']).delete()

print("Creating test data...")

# 1. Создать предметы
subjects = []
subject_names = ['Математика', 'Физика', 'Русский язык', 'История', 'Английский язык']
for name in subject_names:
    subject, created = Subject.objects.get_or_create(name=name)
    subjects.append(subject)
    print(f"✓ Subject: {name}")

# 2. Создать группу
group, created = Group.objects.get_or_create(
    name='10-A',
    academic_year='2024-2025',
    defaults={'description': 'Десятый класс, группа А'}
)
print(f"✓ Group: {group}")

# 3. Создать учителя
teacher_user, created = User.objects.get_or_create(
    username='teacher1',
    defaults={
        'first_name': 'Иван',
        'last_name': 'Сидоров',
        'email': 'teacher1@example.com',
        'role': 'teacher',
        'is_active': True,
    }
)
if created:
    teacher_user.set_password('teacher123')
    teacher_user.save()

teacher, created = Teacher.objects.get_or_create(
    user=teacher_user,
    defaults={'bio': 'Учитель математики и физики'}
)
print(f"✓ Teacher: {teacher_user.get_full_name()}")

# 4. Привязать учителя к предметам
for subject in subjects[:2]:  # Первые два предмета
    TeacherSubject.objects.get_or_create(teacher=teacher, subject=subject)
print(f"✓ Teacher subjects assigned")

# 5. Создать студентов
students = []
for i in range(1, 6):
    student_user, created = User.objects.get_or_create(
        username=f'student{i}',
        defaults={
            'first_name': f'Студент{i}',
            'last_name': f'Иванов{i}',
            'email': f'student{i}@example.com',
            'role': 'student',
            'is_active': True,
        }
    )
    if created:
        student_user.set_password('student123')
        student_user.save()
    
    student, created = Student.objects.get_or_create(
        user=student_user,
        group=group
    )
    students.append(student)
    print(f"✓ Student: {student_user.get_full_name()}")

# 6. Создать расписание
for idx, subject in enumerate(subjects[:2]):
    schedule, created = Schedule.objects.get_or_create(
        group=group,
        subject=subject,
        teacher=teacher,
        weekday=idx,
        start_time='09:00',
        end_time='10:00',
        defaults={'room': f'{100 + idx}'}
    )
    print(f"✓ Schedule: {schedule}")

# 7. Создать уроки
today = timezone.now().date()
schedules = Schedule.objects.filter(group=group)
for schedule in schedules:
    for days in range(7):
        lesson_date = today + timedelta(days=days)
        lesson, created = Lesson.objects.get_or_create(
            schedule=schedule,
            date=lesson_date,
            defaults={'topic': f'Урок по {schedule.subject}'}
        )
        
        # Создать посещаемость для всех студентов
        for student in students:
            attendance, created = Attendance.objects.get_or_create(
                lesson=lesson,
                student=student,
                defaults={'status': 'present'}
            )
print(f"✓ Lessons and attendance records created")

# 8. Создать оценки
import random
for student in students:
    for subject in subjects[:2]:
        for _ in range(5):
            grade = Grade.objects.create(
                student=student,
                subject=subject,
                teacher=teacher,
                value=random.randint(3, 5),
                grade_type=random.choice(['homework', 'test', 'classwork']),
                comment='Хорошо выполнено'
            )
print(f"✓ Grades created")

# 9. Создать домашние задания
from apps.homework.models import StudentHomeworkSubmission
for subject in subjects[:2]:
    homework = Homework.objects.create(
        subject=subject,
        teacher=teacher,
        group=group,
        title=f'Домашнее задание по {subject.name}',
        description=f'Выполните упражнения из учебника по {subject.name}',
        deadline=timezone.now() + timedelta(days=3),
        status='published'
    )
    
    # Создать материалы
    HomeworkMaterial.objects.create(
        homework=homework,
        title='Решение примеров',
        description='Инструкции по решению'
    )
    
    # Создать сдачи студентов
    for student in students:
        submission = StudentHomeworkSubmission.objects.create(
            homework=homework,
            student=student,
            submission_text='Мое решение...',
            status=random.choice(['pending', 'submitted']),
            submitted_at=timezone.now() if random.choice([True, False]) else None
        )

print(f"✓ Homeworks created")

# 10. Создать экзамены
from apps.exams.models import ExamResult
for subject in subjects[:2]:
    exam = Exam.objects.create(
        subject=subject,
        teacher=teacher,
        group=group,
        date=timezone.now() + timedelta(days=14),
        duration_minutes=120,
        location='Аудитория 201',
        description=f'Итоговый экзамен по {subject.name}',
        status='planned'
    )
    
    # Создать результаты экзамена
    for student in students:
        result = ExamResult.objects.create(
            exam=exam,
            student=student,
            grade=random.randint(3, 5),
            comment='Хорошая подготовка',
            points_earned=random.randint(70, 100),
            points_total=100
        )

print(f"✓ Exams created")

print("\n✅ Test data created successfully!")
print("\nYou can now login with:")
print("  Teacher: username='teacher1', password='teacher123'")
print("  Student: username='student1', password='student123'")
