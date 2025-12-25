from venv import logger
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.core.exceptions import ValidationError, PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken # لاستخدام نظام التوكن
import logging
from core_upm.business_logic import UserService 
from core_upm.serializers import UserRegistrationSerializer, UserSerializer 
from rest_framework import viewsets
from django.contrib.auth.models import User

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
class UserRegistrationAPIView(APIView):
    # السماح لأي مستخدم (غير مصادق) بالوصول لصفحة التسجيل
    permission_classes = [AllowAny]
    user_service = UserService()

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # فصل كلمة المرور للتعامل معها بشكل آمن في الـ Service
                password = serializer.validated_data.pop('password')
                user = self.user_service.register_new_user(serializer.validated_data, password)
                
                # إرجاع بيانات المستخدم (باستخدام UserSerializer للعرض)
                return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]
    user_service = UserService()

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user = self.user_service.authenticate_user(username, password)
            
            # إنشاء JWT Tokens (إذا كنت تستخدم Django REST Framework Simple JWT)
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)
            
        except PermissionDenied as e:
            return Response({'detail': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        
        except Exception as e:
            logger.error(f"Login unexpected error: {e}")
            return Response({'detail': 'An unexpected error occurred during login.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)