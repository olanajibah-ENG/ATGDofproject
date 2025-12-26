#!/usr/bin/env python3

import requests
import json
import time

def test_full_flow():
    print("اختبار التدفق الكامل لـ Class Diagram API")
    print("=" * 60)

    base_url = "http://127.0.0.1:8000/api/analysis"

    # 1. إنشاء ملف كود Java للاختبار
    java_code = '''
public class Car {
    private String model;
    private Engine engine;

    public Car(String model) {
        this.model = model;
        this.engine = new Engine(200);
    }

    public void drive() {
        System.out.println("Driving " + model);
    }

    public void setModel(String model) {
        this.model = model;
    }

    public String getModel() {
        return model;
    }
}

class Engine {
    private int horsepower;

    public Engine(int horsepower) {
        this.horsepower = horsepower;
    }

    public void start() {
        System.out.println("Engine started with " + horsepower + " HP");
    }
}
'''

    print("1. إنشاء ملف كود Java للاختبار...")
    create_data = {
        "filename": "TestClassDiagram.java",
        "file_type": "java",
        "content": java_code
    }

    try:
        response = requests.post(f"{base_url}/codefiles/", json=create_data)
        print(f"إنشاء الملف - Status: {response.status_code}")

        if response.status_code == 201:
            result = response.json()
            codefile_id = result['id']
            print(f"✅ تم إنشاء CodeFile بنجاح - ID: {codefile_id}")

            # 2. انتظار التحليل (أو بدء التحليل يدوياً)
            print("\n2. بدء التحليل...")
            analyze_response = requests.post(f"{base_url}/codefiles/{codefile_id}/analyze/")
            print(f"بدء التحليل - Status: {analyze_response.status_code}")

            # انتظار التحليل
            print("\n3. انتظار اكتمال التحليل...")
            time.sleep(3)  # انتظار 3 ثوان

            # 3. الحصول على نتائج التحليل
            print("\n4. الحصول على نتائج التحليل...")
            results_response = requests.get(f"{base_url}/analysis-results/")
            print(f"الحصول على النتائج - Status: {results_response.status_code}")

            if results_response.status_code == 200:
                results = results_response.json()
                print(f"عدد النتائج: {len(results)}")

                if results:
                    # البحث عن النتيجة الخاصة بالملف المُنشأ
                    target_result = None
                    for result in results:
                        if result.get('code_file_id') == codefile_id:
                            target_result = result
                            break

                    if target_result:
                        analysis_result_id = target_result['id']
                        print(f"✅ تم العثور على نتيجة التحليل - ID: {analysis_result_id}")

                        # 4. جرب الـ class diagram endpoint
                        print(f"\n5. جرب الـ class diagram endpoint...")
                        diagram_url = f"{base_url}/analysis-results/{analysis_result_id}/class_diagram/"
                        print(f"URL: {diagram_url}")

                        diagram_response = requests.get(diagram_url)
                        print(f"Class Diagram - Status: {diagram_response.status_code}")

                        if diagram_response.status_code == 200:
                            diagram_data = diagram_response.json()
                            print("✅ نجح الحصول على class diagram!")
                            print("\nالبيانات المُرجعة:")
                            print(json.dumps(diagram_data, indent=2, ensure_ascii=False))

                            # عرض ملخص للفئات
                            if 'class_diagram_data' in diagram_data:
                                classes = diagram_data['class_diagram_data'].get('classes', [])
                                print(f"\n📊 ملخص الفئات المكتشفة: {len(classes)} فئة")
                                for cls in classes:
                                    print(f"  - {cls['name']}: {len(cls.get('methods', []))} طريقة, {len(cls.get('attributes', []))} خاصية")

                        elif diagram_response.status_code == 404:
                            print("❌ 404 - الـ endpoint غير موجود")
                            print("تأكد من أن Django server يعمل وأن الـ URL صحيح")
                        else:
                            print(f"❌ خطأ آخر: {diagram_response.status_code}")
                            print(f"Response: {diagram_response.text}")
                    else:
                        print("❌ لم يتم العثور على نتيجة التحليل")
                        print("قد يحتاج التحليل وقت أطول، جرب انتظار أكثر")
                else:
                    print("❌ لا توجد نتائج تحليل")
            else:
                print(f"❌ فشل في الحصول على النتائج: {results_response.text}")

        else:
            print(f"❌ فشل في إنشاء CodeFile: {response.status_code}")
            print(f"Response: {response.text}")

    except requests.exceptions.ConnectionError:
        print("❌ خطأ في الاتصال")
        print("تأكد من أن Django server يعمل على http://127.0.0.1:8000")
        print("شغل الأمر: cd Ai_project && python manage.py runserver 127.0.0.1:8000")
    except Exception as e:
        print(f"❌ خطأ غير متوقع: {e}")

if __name__ == "__main__":
    test_full_flow()
