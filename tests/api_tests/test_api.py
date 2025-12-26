import requests
import json

# اختبار 1: إرسال كود Python عبر JSON (نسخ لصق)
print("=== اختبار 1: إرسال كود Python عبر JSON ===")
python_code = '''class Car:
    def __init__(self, model):
        self.model = model
        self.engine = Engine(200)

    def drive(self):
        return "Driving"

class Engine:
    def __init__(self, horsepower):
        self.horsepower = horsepower
'''

data = {
    "filename": "test_python_composition.py",
    "file_type": "python",
    "content": python_code
}

try:
    response = requests.post("http://localhost:8002/api/codefiles/", json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    if response.status_code == 201:
        codefile_id = response.json()['id']
        print(f"✅ نجح إنشاء CodeFile مع ID: {codefile_id}")

        # انتظار التحليل
        import time
        time.sleep(5)

        # الحصول على نتائج التحليل
        result_response = requests.get(f"http://localhost:8002/api/analysis-results/{codefile_id}/")
        if result_response.status_code == 200:
            result = result_response.json()
            print("✅ نتائج التحليل:")
            if 'class_diagram_data' in result and result['class_diagram_data']:
                classes = result['class_diagram_data'].get('classes', [])
                for cls in classes:
                    print(f"  - Class: {cls['name']}")
                    if 'associations' in cls and cls['associations']:
                        print(f"    Associations: {cls['associations']}")
        else:
            print(f"❌ فشل في الحصول على نتائج التحليل: {result_response.status_code}")
    else:
        print(f"❌ فشل في إنشاء CodeFile: {response.status_code}")
except Exception as e:
    print(f"❌ خطأ في الاتصال: {e}")

print("\n" + "="*50)

# اختبار 2: رفع ملف Python
print("=== اختبار 2: رفع ملف Python ===")
try:
    with open('test_composition.py', 'rb') as f:
        files = {
            'uploaded_file': ('test_composition.py', f, 'text/plain'),
        }
        data = {
            'filename': 'uploaded_test.py',
            'file_type': 'python'
        }
        response = requests.post("http://localhost:8002/api/codefiles/", files=files, data=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        if response.status_code == 201:
            print("✅ نجح رفع الملف")
        else:
            print(f"❌ فشل في رفع الملف: {response.status_code}")
except Exception as e:
    print(f"❌ خطأ في رفع الملف: {e}")

print("\n" + "="*50)

# اختبار 3: إرسال كود Java
print("=== اختبار 3: إرسال كود Java عبر JSON ===")
java_code = '''public class Car {
    private String model;
    private Engine engine;

    public Car(String model) {
        this.model = model;
        this.engine = new Engine(200);
    }

    public void drive() {
        System.out.println("Driving");
    }
}

class Engine {
    private int horsepower;

    public Engine(int horsepower) {
        this.horsepower = horsepower;
    }
}
'''

data = {
    "filename": "test_java.java",
    "file_type": "java",
    "content": java_code
}

try:
    response = requests.post("http://localhost:8002/api/codefiles/", json=data)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 201:
        print("✅ نجح إرسال كود Java")
        codefile_id = response.json()['id']
        print(f"Java CodeFile ID: {codefile_id}")

        # انتظار التحليل
        import time
        time.sleep(3)

        # الحصول على نتائج التحليل
        result_response = requests.get(f"http://localhost:8002/api/analysis-results/{codefile_id}/")
        if result_response.status_code == 200:
            result = result_response.json()
            print("✅ نتائج تحليل Java:")
            print(f"Status: {result.get('status')}")
            if result.get('error_message'):
                print(f"Error: {result.get('error_message')}")
        else:
            print(f"❌ فشل في الحصول على نتائج التحليل: {result_response.status_code}")
    else:
        print(f"❌ فشل في إرسال كود Java: {response.status_code}")
        print(f"Response: {response.text}")
except Exception as e:
    print(f"❌ خطأ في إرسال كود Java: {e}")
