from rest_framework import permissions


class IsStudent(permissions.BasePermission):
    """Permission for students."""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'student'


class IsTeacher(permissions.BasePermission):
    """Permission for teachers."""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'teacher'


class IsAcademicOffice(permissions.BasePermission):
    """Permission for academic office staff."""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'academic_office'


class IsAdmin(permissions.BasePermission):
    """Permission for admins."""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'admin'


class IsDirector(permissions.BasePermission):
    """Permission for directors."""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'director'


class IsTeacherOrReadOnly(permissions.BasePermission):
    """Permission for teachers with read-only access for others."""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and request.user.role == 'teacher'
