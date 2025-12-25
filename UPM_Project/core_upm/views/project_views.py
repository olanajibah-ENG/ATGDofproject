from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

# تأكد من أن هذا المسار صحيح: core_upm.business_logic
from core_upm.business_logic import ProjectService


# ----------------------------------------------------
# Pagination Configuration
# ----------------------------------------------------
class ProjectPagination(PageNumberPagination):
    """Pagination class for Project list views."""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


# ----------------------------------------------------
# 1. View لإنشاء وسرد المشاريع (GET, POST)
# ----------------------------------------------------
class ProjectListCreateAPIView(ListCreateAPIView):
    """
    سرد جميع المشاريع أو إنشاء مشروع جديد.
    """
    # تحديد الصلاحيات: يتطلب أن يكون المستخدم مصادقاً
    permission_classes = [IsAuthenticated]

    # تحديد pagination class
    pagination_class = ProjectPagination

    def get_queryset(self):
        """
        تصفية المشاريع لعرض مشاريع المستخدم الحالي فقط.
        Filter projects to show only the current user's projects.
        """
        service = ProjectService()
        return service.get_user_projects(user=self.request.user)

    def get_serializer_class(self):
        # الاستيراد المحلي للـ Serializer لتجنب الاعتمادية الدورية
        from core_upm.serializers.project_serializer import ProjectListCreateSerializer
        return ProjectListCreateSerializer

    def perform_create(self, serializer):
        """
        تجاوز عملية الإنشاء لاستخدام خدمة الأعمال (Business Service).
        """
        service = ProjectService()
        # Map serializer validated_data (title/description) to service expected format (project_name/project_description)
        service_data = {
            'project_name': serializer.validated_data.get('project_name'),
            'project_description': serializer.validated_data.get('project_description', '')
        }
        project = service.create_new_project(user=self.request.user, data=service_data)
        # Update serializer instance with created project
        serializer.instance = project


# ----------------------------------------------------
# 2. View للتعديل والحذف والاسترداد (GET, PUT, DELETE)
# ----------------------------------------------------
class ProjectRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    استرداد، تحديث، أو حذف مشروع محدد.
    """
    # تحديد الصلاحيات
    permission_classes = [IsAuthenticated]

    # تحديد حقل البحث في URL
    lookup_field = 'project_id'
    lookup_url_kwarg = 'project_id'

    def get_queryset(self):
        """
        تصفية المشاريع لعرض مشاريع المستخدم الحالي فقط.
        Filter projects to show only the current user's projects.
        """
        service = ProjectService()
        return service.get_user_projects(user=self.request.user) 

    def get_serializer_class(self):
        # الاستيراد المحلي للـ Serializer لتجنب الاعتمادية الدورية
        from core_upm.serializers.project_serializer import ProjectRetrieveUpdateDestroySerializer 
        return ProjectRetrieveUpdateDestroySerializer

    def perform_update(self, serializer):
        """
        تجاوز عملية التحديث لاستخدام خدمة الأعمال.
        """
        service = ProjectService()
        project = self.get_object()
        # Map serializer validated_data (title/description) to service expected format (project_name/project_description)
        service_data = {}
        if 'project_name' in serializer.validated_data:
            service_data['project_name'] = serializer.validated_data['project_name']
        if 'project_description' in serializer.validated_data:
            service_data['project_description'] = serializer.validated_data['project_description']
        updated_project = service.update_project(
            project=project,
            data=service_data,
            user=self.request.user
        )
        # Update serializer instance with updated project
        serializer.instance = updated_project
        
    def perform_destroy(self, instance):
        """
        تجاوز عملية الحذف لاستخدام خدمة الأعمال.
        """
        service = ProjectService()
        project_id = str(instance.project_id)
        service.delete_project(project_id=project_id, user=self.request.user)