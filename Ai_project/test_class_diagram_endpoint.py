#!/usr/bin/env python3

import os
import sys
import django

# إعداد Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Ai_project.settings')
django.setup()

from rest_framework.test import APIRequestFactory, APIClient
from core_ai.views import AnalysisResultViewSet
from django.test import TestCase

def test_class_diagram_endpoint():
    print("اختبار endpoint class_diagram...")
    print("=" * 50)

    # إنشاء client للاختبار
    client = APIClient()

    # محاولة الوصول للـ endpoint
    url = '/api/analysis/analysis-results/507f1f77bcf86cd799439011/class_diagram/'

    try:
        response = client.get(url)
        print(f"Response status: {response.status_code}")
        print(f"Response data: {response.data}")

        if response.status_code == 200:
            print("✅ SUCCESS: Endpoint is working!")
        else:
            print(f"❌ ERROR: Status {response.status_code}")

    except Exception as e:
        print(f"❌ ERROR: {str(e)}")

    # محاولة الوصول للـ endpoint الأساسي
    print("\n" + "-" * 30)
    print("اختبار endpoint الأساسي...")

    try:
        response = client.get('/api/analysis/analysis-results/')
        print(f"Basic endpoint status: {response.status_code}")

        if response.status_code == 200:
            print("✅ Basic endpoint is working!")
        else:
            print(f"❌ Basic endpoint error: Status {response.status_code}")

    except Exception as e:
        print(f"❌ Basic endpoint ERROR: {str(e)}")

if __name__ == "__main__":
    test_class_diagram_endpoint()
