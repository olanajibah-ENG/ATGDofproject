from os import name
from django.shortcuts import get_object_or_404
from core_upm.models import CodeArtifact, Project # الاستيراد من طبقة Models
from django.db import IntegrityError
from django.db.models import QuerySet
import uuid
import logging
from core_upm import external_storage

logger = logging.getLogger(name)
class ArtifactRepository:

    def save_content_externally(self, content: str) -> str:
        """Saves the raw code content to the simulated external storage."""
        # Delegating the task to the dedicated module
        return external_storage.save_code_content(content)
        
    def fetch_content_externally(self, storage_reference: str) -> str:
        """Fetches the raw code content from the simulated external storage."""
        # Delegating the task to the dedicated module
        return external_storage.fetch_code_content(storage_reference)
        
    def create_artifact(self, project: Project, file_name: str, code_language: str, code_version: str, storage_ref: str) -> CodeArtifact:
        """Creates a new CodeArtifact metadata entry in the database."""
        # تم التأكد من استخدام code_language و code_version
        return CodeArtifact.objects.create(
            project=project,
            file_name=file_name,
            code_language=code_language, 
            code_version=code_version,   
            storage_reference=storage_ref
        )

    def get_artifacts_by_project(self, project: Project) -> QuerySet[CodeArtifact]:
        """Retrieves all artifact metadata for a given project."""
        return CodeArtifact.objects.filter(project=project).order_by('-upload_date')

    def get_artifact_by_id(self, code_id: str) -> CodeArtifact:
        """Retrieves a single CodeArtifact metadata by ID or raises 404."""
        return get_object_or_404(CodeArtifact, code_id=code_id)

    # 👈 إضافة جديدة: لحذف المحتوى الخارجي
    def delete_content_externally(self, storage_reference: str) -> None:
        """Deletes the raw code content from the simulated external storage."""
        # Delegating the task to the dedicated module (نفترض وجود الدالة)
        external_storage.delete_code_content(storage_reference) 

    # 👈 إضافة جديدة: لحذف الـ Artifact
    def delete_artifact(self, artifact: CodeArtifact) -> None:
        """Deletes a specific CodeArtifact instance."""
        artifact.delete()
        
    # 👈 إضافة جديدة: لتحديث بيانات الـ Artifact (الميتا داتا فقط)
    def update_artifact_metadata(self, artifact: CodeArtifact, file_name: str = None, code_language: str = None, code_version: str = None) -> CodeArtifact:
        """Updates artifact metadata (not content)."""
        if file_name is not None:
            artifact.file_name = file_name
        if code_language is not None:
            artifact.code_language = code_language
        if code_version is not None:
            artifact.code_version = code_version
            
        artifact.save()
        return artifact