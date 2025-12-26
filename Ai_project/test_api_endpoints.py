#!/usr/bin/env python3

import requests
import json

def test_api_endpoints():
    base_url = "http://127.0.0.1:8000/api/analysis"

    print("اختبار API endpoints...")
    print("=" * 50)

    # اختبار 1: الحصول على جميع analysis results
    print("1. اختبار الحصول على جميع analysis results:")
    try:
        response = requests.get(f"{base_url}/analysis-results/")
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"عدد النتائج: {len(data)}")

            if data:
                # عرض أول نتيجة
                first_result = data[0]
                result_id = first_result.get('id')
                print(f"أول نتيجة ID: {result_id}")

                # اختبار 2: الحصول على class diagram للنتيجة الأولى
                print(f"\n2. اختبار الحصول على class diagram للنتيجة {result_id}:")
                diagram_url = f"{base_url}/analysis-results/{result_id}/class_diagram/"
                print(f"URL: {diagram_url}")

                diagram_response = requests.get(diagram_url)
                print(f"Status: {diagram_response.status_code}")

                if diagram_response.status_code == 200:
                    diagram_data = diagram_response.json()
                    print("✅ نجح الحصول على class diagram!")
                    print(f"البيانات: {json.dumps(diagram_data, indent=2, ensure_ascii=False)}")
                else:
                    print(f"❌ فشل في الحصول على class diagram: {diagram_response.text}")

                # اختبار 3: جرب الـ ID المحدد من المستخدم
                user_id = "694195fdee8b7047cd3f4b3e"
                print(f"\n3. اختبار الـ ID المحدد من المستخدم: {user_id}")
                user_diagram_url = f"{base_url}/analysis-results/{user_id}/class_diagram/"
                print(f"URL: {user_diagram_url}")

                user_response = requests.get(user_diagram_url)
                print(f"Status: {user_response.status_code}")

                if user_response.status_code == 200:
                    user_data = user_response.json()
                    print("✅ نجح الحصول على class diagram للـ ID المحدد!")
                    print(f"البيانات: {json.dumps(user_data, indent=2, ensure_ascii=False)}")
                elif user_response.status_code == 404:
                    print("❌ النتيجة غير موجودة (404)")
                    print("تأكد من صحة الـ ID أو أن النتيجة موجودة في قاعدة البيانات")
                else:
                    print(f"❌ خطأ آخر: {user_response.status_code} - {user_response.text}")

            else:
                print("⚠️ لا توجد نتائج تحليل في قاعدة البيانات")
                print("حاول إنشاء ملف كود وتحليله أولاً")
        else:
            print(f"❌ فشل في الحصول على analysis results: {response.text}")

    except Exception as e:
        print(f"❌ خطأ في الاتصال: {e}")
        print("تأكد من أن Django server يعمل على http://127.0.0.1:8000")

if __name__ == "__main__":
    test_api_endpoints()
