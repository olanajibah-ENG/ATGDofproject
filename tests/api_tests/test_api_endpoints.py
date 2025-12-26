#!/usr/bin/env python3

import requests
import json

def test_api_endpoints():
    base_url = "http://127.0.0.1:8000/api/analysis"

    print("اختبار API endpoints...")
    print("=" * 50)

    # 1. الحصول على جميع analysis results
    print("1. الحصول على جميع analysis results:")
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

                # 2. اختبار class diagram للنتيجة الأولى
                print(f"\n2. اختبار class diagram للنتيجة {result_id}:")
                diagram_url = f"{base_url}/analysis-results/{result_id}/class_diagram/"
                print(f"URL: {diagram_url}")

                diagram_response = requests.get(diagram_url)
                print(f"Status: {diagram_response.status_code}")

                if diagram_response.status_code == 200:
                    diagram_data = diagram_response.json()
                    print("✅ نجح الحصول على class diagram!")
                    print(f"البيانات: {json.dumps(diagram_data, indent=2, ensure_ascii=False)}")

                elif diagram_response.status_code == 404:
                    print("❌ 404 - الـ endpoint غير موجود")
                    print("تأكد من أن Django server يعمل وأن الـ URL صحيح")
                else:
                    print(f"❌ خطأ آخر: {diagram_response.status_code}")
                    print(f"Response: {diagram_response.text}")

            else:
                print("⚠️ لا توجد نتائج تحليل في قاعدة البيانات")
                print("أنشئ ملف كود أولاً ثم قم بتحليله")

        else:
            print(f"❌ فشل في الحصول على analysis results: {response.text}")

    except requests.exceptions.ConnectionError:
        print("❌ خطأ في الاتصال")
        print("تأكد من أن Django server يعمل على http://127.0.0.1:8000")
    except Exception as e:
        print(f"❌ خطأ غير متوقع: {e}")

if __name__ == "__main__":
    test_api_endpoints()
