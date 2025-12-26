# core_upm/views/artifact_views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import PermissionDenied, ValidationError

# الاستيراد من طبقة Business Logic و Serializers
from core_upm.business_logic import artifact_service 
from core_upm.serializers import CodeArtifactSerializer, CodeArtifactDetailSerializer
# 👈 استيراد نموذج CodeArtifact للتعامل مع الـ Exceptions
from core_upm.models.artifact import CodeArtifact 


class ArtifactRetrieveUpdateDestroyAPIView(APIView):
    """View لجلب، تحديث، وحذف مادة برمجية فردية."""
    permission_classes = [IsAuthenticated]
    artifact_service = artifact_service

    def get(self, request, code_id):
        # جلب الـ Artifact (Retrieve)
        try:
            # استخدام دالة جلب الـ Artifact والمحتوى مع التحقق من الصلاحيات
            artifact = self.artifact_service.retrieve_artifact_with_content(code_id, request.user)
            # استخدام Serializer التفصيلي لعرض المحتوى
            serializer = CodeArtifactDetailSerializer(artifact) 
            return Response(serializer.data)
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
        # 👈 تصحيح: استخدام CodeArtifact.DoesNotExist
        except CodeArtifact.DoesNotExist: 
            return Response({"detail": "Artifact not found."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, code_id):
        # لتعديل الـ Artifact (Update)
        try:
            # جلب الـ Artifact والتحقق من الصلاحيات
            artifact = self.artifact_service.get_artifact_by_id_if_authorized(code_id, request.user)
            
            # نستخدم CodeArtifactSerializer لتعديل الميتا-داتا فقط
            serializer = CodeArtifactSerializer(artifact, data=request.data, partial=True)
            if serializer.is_valid():
                # تمرير البيانات لطبقة الخدمة للتحديث
                updated_artifact = self.artifact_service.update_artifact_metadata(artifact, serializer.validated_data) 
                return Response(CodeArtifactSerializer(updated_artifact).data)
                
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        # 👈 تصحيح: استخدام CodeArtifact.DoesNotExist
        except CodeArtifact.DoesNotExist:
            return Response({"detail": "Artifact not found."}, status=status.HTTP_404_NOT_FOUND)


    def delete(self, request, code_id):
        # لحذف الـ Artifact (Destroy)
        try:
            # طبقة الخدمة تتولى الحذف والتحقق من الملكية
            self.artifact_service.delete_artifact(code_id, request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
        # 👈 تصحيح: استخدام CodeArtifact.DoesNotExist
        except CodeArtifact.DoesNotExist:
            return Response({"detail": "Artifact not found."}, status=status.HTTP_404_NOT_FOUND)
class ArtifactListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    artifact_service = artifact_service

    def get(self, request, project_id):
        # جلب جميع الـ Artifacts لمشروع معين
        try:
            artifacts = self.artifact_service.get_artifacts_by_project(project_id, request.user)
            serializer = CodeArtifactSerializer(artifacts, many=True)
            return Response(serializer.data)
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, project_id):
        # إنشاء مادة برمجية جديدة في مشروع معين
        serializer = CodeArtifactSerializer(data=request.data)
        if serializer.is_valid():
            try:
                artifact = self.artifact_service.create_artifact_in_project(
                    project_id,
                    request.user,
                    serializer.validated_data
                )
                return Response(CodeArtifactSerializer(artifact).data, status=status.HTTP_201_CREATED)
            except PermissionDenied as e:
                return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
            except ValidationError as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class ArtifactRetrieveAPIView(APIView):
    """View لجلب مادة برمجية فردية مع المحتوى."""
    permission_classes = [IsAuthenticated]
    artifact_service = artifact_service

    def get(self, request, code_id):
        # جلب الـ Artifact (Retrieve)
        try:
            # استخدام دالة جلب الـ Artifact والمحتوى مع التحقق من الصلاحيات
            artifact = self.artifact_service.retrieve_artifact_with_content(code_id, request.user)
            # استخدام Serializer التفصيلي لعرض المحتوى
            serializer = CodeArtifactDetailSerializer(artifact) 
            return Response(serializer.data)
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
        # 👈 تصحيح: استخدام CodeArtifact.DoesNotExist
        except CodeArtifact.DoesNotExist: 
            return Response({"detail": "Artifact not found."}, status=status.HTTP_404_NOT_FOUND)