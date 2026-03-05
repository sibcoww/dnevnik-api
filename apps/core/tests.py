from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.accounts.models import Teacher, Student
from apps.academics.models import Subject, Group, Schedule, Lesson
from apps.journal.models import Attendance, Grade
from datetime import timedelta
from django.utils import timezone

User = get_user_model()


class UserModelTestCase(TestCase):
    """Test cases for User model."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            first_name='Test',
            last_name='User',
            role='teacher'
        )
    
    def test_user_creation(self):
        """Test user creation."""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.role, 'teacher')
        self.assertTrue(self.user.is_active)
    
    def test_user_full_name(self):
        """Test user full name."""
        self.assertEqual(self.user.get_full_name(), 'Test User')
    
    def test_password_hashing(self):
        """Test password hashing."""
        self.assertTrue(self.user.check_password('testpass123'))
        self.assertFalse(self.user.check_password('wrongpassword'))


class AcademicsModelTestCase(TestCase):
    """Test cases for academic models."""
    
    def setUp(self):
        self.subject = Subject.objects.create(
            name='Mathematics',
            description='Basic math'
        )
        
        self.group = Group.objects.create(
            name='10-A',
            academic_year='2024-2025'
        )
        
        self.teacher_user = User.objects.create_user(
            username='teacher1',
            password='pass123',
            first_name='John',
            last_name='Doe',
            role='teacher'
        )
        
        self.teacher = Teacher.objects.create(user=self.teacher_user)
        
        self.schedule = Schedule.objects.create(
            group=self.group,
            subject=self.subject,
            teacher=self.teacher,
            weekday=0,
            start_time='09:00',
            end_time='10:00'
        )
    
    def test_subject_creation(self):
        """Test subject creation."""
        self.assertEqual(self.subject.name, 'Mathematics')
    
    def test_group_creation(self):
        """Test group creation."""
        self.assertEqual(self.group.name, '10-A')
        self.assertEqual(self.group.academic_year, '2024-2025')
    
    def test_schedule_creation(self):
        """Test schedule creation."""
        self.assertEqual(self.schedule.subject, self.subject)
        self.assertEqual(self.schedule.group, self.group)
        self.assertEqual(self.schedule.teacher, self.teacher)
    
    def test_lesson_creation(self):
        """Test lesson creation."""
        today = timezone.now().date()
        lesson = Lesson.objects.create(
            schedule=self.schedule,
            date=today,
            topic='Introduction'
        )
        self.assertEqual(lesson.schedule, self.schedule)
        self.assertEqual(lesson.date, today)


class JournalModelTestCase(TestCase):
    """Test cases for journal models."""
    
    def setUp(self):
        # Create subject and group
        self.subject = Subject.objects.create(name='Mathematics')
        self.group = Group.objects.create(name='10-A', academic_year='2024-2025')
        
        # Create teacher
        self.teacher_user = User.objects.create_user(
            username='teacher1',
            password='pass123',
            first_name='John',
            last_name='Doe',
            role='teacher'
        )
        self.teacher = Teacher.objects.create(user=self.teacher_user)
        
        # Create student
        self.student_user = User.objects.create_user(
            username='student1',
            password='pass123',
            first_name='Jane',
            last_name='Smith',
            role='student'
        )
        self.student = Student.objects.create(user=self.student_user, group=self.group)
        
        # Create schedule and lesson
        self.schedule = Schedule.objects.create(
            group=self.group,
            subject=self.subject,
            teacher=self.teacher,
            weekday=0,
            start_time='09:00',
            end_time='10:00'
        )
        
        today = timezone.now().date()
        self.lesson = Lesson.objects.create(
            schedule=self.schedule,
            date=today,
            topic='Test Lesson'
        )
    
    def test_attendance_creation(self):
        """Test attendance creation."""
        attendance = Attendance.objects.create(
            lesson=self.lesson,
            student=self.student,
            status='present'
        )
        self.assertEqual(attendance.lesson, self.lesson)
        self.assertEqual(attendance.student, self.student)
        self.assertEqual(attendance.status, 'present')
    
    def test_grade_creation(self):
        """Test grade creation."""
        grade = Grade.objects.create(
            student=self.student,
            subject=self.subject,
            teacher=self.teacher,
            value=5,
            grade_type='test'
        )
        self.assertEqual(grade.student, self.student)
        self.assertEqual(grade.value, 5)


class APIAuthenticationTestCase(TestCase):
    """Test cases for API authentication."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            first_name='Test',
            last_name='User',
            role='teacher'
        )
    
    def test_login_endpoint(self):
        """Test login endpoint."""
        response = self.client.post(
            '/api/v1/auth/login/',
            {'username': 'testuser', 'password': 'testpass123'},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.json())
        self.assertIn('refresh', response.json())
