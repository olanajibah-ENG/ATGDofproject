import requests
import json

def test_upm_ai_connection():
    """اختبار الاتصال بين UPM و AI services"""

    print("=== اختبار الاتصال بين UPM و AI ===")

    # اختبار 1: محاولة إرسال طلب مباشر لـ AI service
    print("\n1. اختبار إرسال طلب مباشر لـ AI service...")

    ai_url = "http://localhost:8002/api/analysis/codefiles/"
    test_data = {
        "filename": "test_connection.py",
        "file_type": "python",
        "content": "print('Hello from UPM test')",
        "source_project_id": "test-project-123"
    }

    try:
        response = requests.post(ai_url, json=test_data, timeout=10)
        print(f"AI Service Response: {response.status_code}")

        if response.status_code == 201:
            result = response.json()
            codefile_id = result.get('id')
            print("✓ تم إنشاء CodeFile بنجاح!")
            print(f"  CodeFile ID: {codefile_id}")

            # اختبار 2: التحقق من وجود Analysis Job
            print("\n2. التحقق من Analysis Jobs...")
            jobs_url = "http://localhost:8002/api/analysis/analysis-jobs/"
            jobs_response = requests.get(jobs_url, timeout=5)

            if jobs_response.status_code == 200:
                jobs = jobs_response.json()
                print(f"✓ تم العثور على {len(jobs)} analysis job")

                # البحث عن job الخاص بـ codefile_id
                found_job = None
                for job in jobs:
                    if str(job.get('code_file_id', '')) == str(codefile_id):
                        found_job = job
                        break

                if found_job:
                    print("✓ تم العثور على analysis job لهذا الملف!")
                    print(f"  Job Status: {found_job.get('status')}")
                    print(f"  Created At: {found_job.get('created_at')}")

                    # انتظار قليل ثم التحقق مرة أخرى
                    import time
                    print("انتظار 10 ثوانٍ للتحليل...")
                    time.sleep(10)

                    jobs_response2 = requests.get(jobs_url, timeout=5)
                    if jobs_response2.status_code == 200:
                        jobs2 = jobs_response2.json()
                        for job in jobs2:
                            if str(job.get('code_file_id', '')) == str(codefile_id):
                                print(f"✓ Job Status الآن: {job.get('status')}")
                                break
                else:
                    print("✗ لم يتم العثور على analysis job لهذا الملف")
                    print("Analysis Jobs الموجودة:")
                    for job in jobs[:3]:  # أظهر أول 3 jobs فقط
                        print(f"  - ID: {job.get('id')}, CodeFile: {job.get('code_file_id')}, Status: {job.get('status')}")
            else:
                print(f"✗ فشل في الحصول على Analysis Jobs: {jobs_response.status_code}")

        else:
            print(f"✗ فشل في إنشاء CodeFile: {response.status_code}")
            print(f"Response: {response.text}")

    except requests.exceptions.ConnectionError:
        print("✗ لا يمكن الاتصال بـ AI service على localhost:8002")
        print("تأكد من أن AI container يعمل")
    except Exception as e:
        print(f"✗ خطأ في الاختبار: {e}")

    # اختبار 3: محاولة الاتصال عبر container network
    print("\n3. اختبار الاتصال عبر Docker network...")

    # محاولة الاتصال بـ AI service عبر container name (إذا كنا داخل container)
    try:
        ai_container_url = "http://ai_web:8000/api/analysis/codefiles/"
        response = requests.post(ai_container_url, json=test_data, timeout=5)

        if response.status_code == 201:
            print("✓ الاتصال عبر Docker network يعمل!")
        else:
            print(f"الاتصال عبر Docker network: {response.status_code}")
    except:
        print("✗ لا يمكن الاتصال عبر Docker network (طبيعي إذا كنا خارج containers)")

    print("\n=== نهاية الاختبار ===")

if __name__ == "__main__":
    test_upm_ai_connection()
