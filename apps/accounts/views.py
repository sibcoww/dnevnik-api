from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, Teacher, Student
from .serializers import (
    CustomTokenObtainPairSerializer, UserSerializer,
    UserCreateSerializer, UserUpdateSerializer,
    TeacherSerializer, StudentSerializer
)
from apps.core.permissions import IsAdmin


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom JWT token view."""
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]


class UserViewSet(viewsets.ModelViewSet):
    """User management viewset (admin only)."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['partial_update', 'update']:
            return UserUpdateSerializer
        return UserSerializer
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Get current user data."""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        """Change user password."""
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        
        if not old_password or not new_password:
            return Response(
                {'error': 'Both old_password and new_password are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not user.check_password(old_password):
            return Response(
                {'error': 'Old password is incorrect.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.set_password(new_password)
        user.save()
        
        return Response({'message': 'Password changed successfully.'})


class TeacherViewSet(viewsets.ReadOnlyModelViewSet):
    """Teacher viewset."""
    queryset = Teacher.objects.select_related('user')
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['user__first_name', 'user__last_name']
    search_fields = ['user__first_name', 'user__last_name', 'user__email']


class StudentViewSet(viewsets.ReadOnlyModelViewSet):
    """Student viewset."""
    queryset = Student.objects.select_related('user', 'group')
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['group']
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'group__name']
