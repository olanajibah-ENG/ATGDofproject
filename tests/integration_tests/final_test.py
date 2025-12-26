import requests
import time

BASE_URL = "http://localhost:8002/api/analysis"

print("=== نظام تحليل الكود - اختبار شامل ===")
print()

# Test 1: Python code with composition relationships via JSON
print("1. اختبار تحليل كود Python مع علاقات تركيب (عبر JSON):")

python_code = '''
class Engine:
    def __init__(self, horsepower):
        self.horsepower = horsepower

    def start(self):
        return f"Engine with {self.horsepower}HP started"

class Car:
    def __init__(self, model):
        self.model = model
        self.engine = Engine(200)  # Composition relationship

    def drive(self):
        return f"Driving {self.model}"

    def get_power(self):
        return self.engine.horsepower
'''

data = {
    "filename": "test_composition.py",
    "file_type": "python",
    "content": python_code
}

try:
    response = requests.post(f"{BASE_URL}/codefiles/", json=data)
    print(f"   Status: {response.status_code}")

    if response.status_code == 201:
        result = response.json()
        codefile_id = result['id']
        print(f"   ✓ تم إنشاء CodeFile: {codefile_id}")

        # Analyze the code
        analyze_response = requests.post(f"{BASE_URL}/codefiles/{codefile_id}/analyze/")
        print(f"   تحليل: {analyze_response.status_code}")

        # Wait and get results
        time.sleep(2)
        results_response = requests.get(f"{BASE_URL}/analysis-results/")
        if results_response.status_code == 200:
            results = results_response.json()
            for result in results:
                if result.get('code_file_id') == codefile_id:
                    print(f"   ✓ تم العثور على نتائج التحليل")
                    if 'class_diagram_data' in result:
                        classes = result['class_diagram_data'].get('classes', [])
                        print(f"   📊 فئات مكتشفة: {len(classes)}")
                        for cls in classes:
                            print(f"      - {cls['name']}: {len(cls.get('methods', []))} طريقة")
                            associations = cls.get('associations', [])
                            if associations:
                                print(f"        علاقات: {len(associations)}")
                    break
    else:
        print(f"   ✗ فشل في إنشاء CodeFile: {response.text}")

except Exception as e:
    print(f"   ✗ خطأ: {e}")

print()

# Test 2: Java code with composition relationships via JSON
print("2. اختبار تحليل كود Java مع علاقات تركيب (عبر JSON):")

java_code = '''
public class Engine {
    private int horsepower;

    public Engine(int hp) {
        this.horsepower = hp;
    }

    public void start() {
        System.out.println("Engine started");
    }
}

public class Car {
    private String model;
    private Engine engine;

    public Car(String model) {
        this.model = model;
        this.engine = new Engine(250);  // Composition
    }

    public void drive() {
        System.out.println("Driving " + model);
    }

    public int getHorsepower() {
        return engine.horsepower;
    }
}
'''

data2 = {
    "filename": "TestComposition.java",
    "file_type": "java",
    "content": java_code
}

try:
    response2 = requests.post(f"{BASE_URL}/codefiles/", json=data2)
    print(f"   Status: {response2.status_code}")

    if response2.status_code == 201:
        result2 = response2.json()
        codefile_id2 = result2['id']
        print(f"   ✓ تم إنشاء CodeFile: {codefile_id2}")

        # Analyze
        analyze_response2 = requests.post(f"{BASE_URL}/codefiles/{codefile_id2}/analyze/")
        print(f"   تحليل: {analyze_response2.status_code}")

        # Wait and get results
        time.sleep(3)
        results_response2 = requests.get(f"{BASE_URL}/analysis-results/")
        if results_response2.status_code == 200:
            results2 = results_response2.json()
            for result in results2:
                if result.get('code_file_id') == codefile_id2:
                    print(f"   ✓ تم العثور على نتائج التحليل")
                    if 'class_diagram_data' in result:
                        classes2 = result['class_diagram_data'].get('classes', [])
                        print(f"   📊 فئات مكتشفة: {len(classes2)}")
                        for cls in classes2:
                            print(f"      - {cls['name']}: {len(cls.get('methods', []))} طريقة, {len(cls.get('attributes', []))} خاصية")
                            associations = cls.get('associations', [])
                            if associations:
                                print(f"        علاقات: {len(associations)}")
                    break
    else:
        print(f"   ✗ فشل في إنشاء CodeFile: {response2.text}")

except Exception as e:
    print(f"   ✗ خطأ: {e}")

print()
print("=== انتهى الاختبار الشامل ===")
print("تأكد من تشغيل Django server و MongoDB و Redis")
