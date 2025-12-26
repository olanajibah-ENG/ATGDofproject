from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView
from core_upm.views import (
    UserRegistrationAPIView, 
    UserLoginAPIView,
    ProjectListCreateAPIView,
    ProjectRetrieveUpdateDestroyAPIView,
    ArtifactListCreateAPIView,
    ArtifactRetrieveAPIView
)

urlpatterns = [
    # ------------------
    # 1. Authentication Paths
    # ------------------
    path('signup/', UserRegistrationAPIView.as_view(), name='register'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # ------------------
    # 2. Project Management Paths
    # ------------------
    path('projects/', ProjectListCreateAPIView.as_view(), name='project-list-create'),
    path('projects/<uuid:project_id>/', ProjectRetrieveUpdateDestroyAPIView.as_view(), name='project-detail'),
    
    # ------------------
    # 3. Artifact Management Paths
    # ------------------
    path('projects/<uuid:project_id>/artifacts/', ArtifactListCreateAPIView.as_view(), name='artifact-list-create'),
    path('artifacts/<uuid:code_id>/', ArtifactRetrieveAPIView.as_view(), name='artifact-detail'),
]