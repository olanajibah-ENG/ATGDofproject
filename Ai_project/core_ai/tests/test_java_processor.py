#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from core_ai.language_processors.java_processor import JavaProcessor

def test_java_processor():
    # قراءة ملف Java التجريبي
    with open(os.path.join(os.path.dirname(__file__), 'test_java.java'), 'r', encoding='utf-8') as f:
        java_code = f.read()

    print("اختبار معالج Java...")
    print("=" * 50)

    # إنشاء المعالج
    processor = JavaProcessor()

    # اختبار التحليل
    print("1. اختبار تحليل الكود:")
    ast_data = processor.parse_source_code(java_code)
    if ast_data.get("error"):
        print(f"خطأ في التحليل: {ast_data['error']}")
        return

    print("✓ تم تحليل الكود بنجاح")

    # اختبار استخراج الخصائص
    print("\n2. اختبار استخراج الخصائص:")
    features = processor.extract_features(ast_data)
    print(f"عدد الأسطر: {features.get('lines_of_code', 0)}")
    print(f"عدد الطرق: {features.get('methods', 0)}")

    # اختبار استخراج التبعيات
    print("\n3. اختبار استخراج التبعيات:")
    dependencies = processor.extract_dependencies(ast_data)
    print(f"التبعيات المستخرجة: {dependencies}")

    # اختبار التحليل الدلالي
    print("\n4. اختبار التحليل الدلالي:")
    semantic_issues = processor.perform_semantic_analysis(ast_data, features)
    print(f"عدد المشاكل المكتشفة: {len(semantic_issues.get('issues', []))}")
    for issue in semantic_issues.get('issues', []):
        print(f"  - {issue['type']}: {issue['message']} (السطر: {issue.get('line', '?')})")

    # اختبار إنشاء بيانات مخطط الفئات
    print("\n5. اختبار إنشاء بيانات مخطط الفئات:")
    class_diagram_data = processor.generate_class_diagram_data(ast_data, features)
    print(f"عدد الفئات المستخرجة: {len(class_diagram_data.get('classes', []))}")
    for cls in class_diagram_data.get('classes', []):
        print(f"  - فئة: {cls['name']}")
        print(f"    طرق: {len(cls.get('methods', []))}")
        print(f"    خصائص: {len(cls.get('attributes', []))}")
        print(f"    علاقات: {len(cls.get('associations', []))}")

    # اختبار إنشاء بيانات الرسم البياني للتبعيات
    print("\n6. اختبار إنشاء بيانات الرسم البياني للتبعيات:")
    dependency_graph_data = processor.generate_dependency_graph_data(ast_data, features)
    print(f"عدد العقد: {len(dependency_graph_data.get('nodes', []))}")
    print(f"عدد الحواف: {len(dependency_graph_data.get('edges', []))}")

    print("\n" + "=" * 50)
    print("انتهى الاختبار!")

if __name__ == "__main__":
    test_java_processor()
