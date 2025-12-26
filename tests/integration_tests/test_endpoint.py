#!/usr/bin/env python3

import os
import sys
import django
from django.conf import settings

# إعداد Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Ai_project.settings')
sys.path.append('Ai_project')
django.setup()

from rest_framework.test import APIRequestFactory
from core_ai.views import AnalysisResultViewSet

def test_class_diagram_endpoint():
    print("اختبار endpoint class_diagram...")
    print("=" * 50)

    # إنشاء request factory
    factory = APIRequestFactory()

    # إنشاء view instance
    view = AnalysisResultViewSet()
    view.basename = 'analysis-result'

    # إنشاء request
    request = factory.get('/api/analysis/analysis-results/507f1f77bcf86cd799439011/class_diagram/')

    try:
        # محاولة استدعاء الـ method
        response = view.class_diagram(request, pk='507f1f77bcf86cd799439011')
        print('✅ SUCCESS: Endpoint is accessible')
        print('Response status:', response.status_code)
        print('Response data keys:', list(response.data.keys()) if hasattr(response, 'data') else 'No data')

    except Exception as e:
        print('❌ ERROR:', str(e))
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_class_diagram_endpoint()
