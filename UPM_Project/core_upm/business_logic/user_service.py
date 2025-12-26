from os import name
from django.core.exceptions import PermissionDenied, ValidationError
from django.contrib.auth import authenticate # للاستخدام في منطق تسجيل الدخول
from core_upm.repositories import UserRepository # استيراد الـ Repository
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(name)


class UserService:
    """
    Handles user authentication and registration logic. 
    Uses UserRepository for data access.
    """
    def __init__(self):
        self.user_repo = UserRepository()
    
    def register_new_user(self, user_data: dict, password: str) -> User:
        """
        Applies registration rules and uses the repository to create the user.
        """
        if self.user_repo.user_exists_by_username(user_data['username']):
            raise ValidationError("Username already taken.")
        if self.user_repo.user_exists_by_email(user_data['email']):
            raise ValidationError("A user with that email already exists.")
            
        try:
            # Use repository to handle creation and password hashing
            user = self.user_repo.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=password
            )
            return user
        except Exception as e:
            logger.error(f"User registration error: {e}")
            # Re-raise as a generic validation error for the view to catch
            raise ValidationError(f"Registration failed: {str(e)}")

    def authenticate_user(self, username: str, password: str) -> User:
        """
        Authenticates user credentials.
        """
        # We rely on Django's authenticate, which implicitly uses the repository model
        user = authenticate(username=username, password=password)
        
        if user is None or not user.is_active:
            raise PermissionDenied("Invalid credentials or inactive account.")
             
        return user