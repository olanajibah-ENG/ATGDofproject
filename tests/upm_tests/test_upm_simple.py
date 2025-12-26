import requests

# اختبار بسيط لرفع ملف كود
BASE_URL = "http://localhost:8001/api/upm"

print("=== اختبار رفع ملف كود بسيط ===")

# 1. تسجيل الدخول
login_data = {
    "username": "testuser2",
    "password": "testpass123"
}

try:
    login_response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
    print(f"Login Status: {login_response.status_code}")

    if login_response.status_code == 200:
        login_result = login_response.json()
        token = login_result.get('access')

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        print("✓ تم تسجيل الدخول بنجاح")

        # 2. إنشاء مشروع
        project_data = {
            "name": "Simple Test Project",
            "description": "مشروع للاختبار البسيط"
        }

        project_response = requests.post(f"{BASE_URL}/projects/", json=project_data, headers=headers)
        print(f"Project Creation Status: {project_response.status_code}")

        if project_response.status_code == 201:
            project = project_response.json()
            project_id = project.get('id')
            print(f"✓ تم إنشاء المشروع: {project_id}")

            # 3. رفع ملف كود
            code_content = '''
def hello_world():
    print("Hello from UPM simple test")
    return "success"

if __name__ == "__main__":
    hello_world()
'''

            artifact_data = {
                "project_id": project_id,
                "name": "Simple Code File",
                "description": "ملف كود بسيط للاختبار",
                "artifact_type": "code",
                "content": code_content,
                "file_type": "python"
            }

            artifact_response = requests.post(f"{BASE_URL}/artifacts/", json=artifact_data, headers=headers)
            print(f"Artifact Upload Status: {artifact_response.status_code}")

            if artifact_response.status_code == 201:
                artifact = artifact_response.json()
                print(f"✓ تم رفع الملف بنجاح: {artifact.get('id')}")

                # 4. إرسال للتحليل
                ai_data = {
                    "content": code_content,
                    "file_type": "python",
                    "filename": "simple_test.py",
                    "artifact_id": artifact.get('id')
                }

                ai_urls = [
                    "http://localhost:8002/api/analysis/codefiles/",
                    "http://ai_web:8000/api/analysis/codefiles/"
                ]

                ai_sent = False
                for ai_url in ai_urls:
                    try:
                        print(f"محاولة إرسال لـ AI: {ai_url}")
                        ai_response = requests.post(ai_url, json=ai_data, timeout=10)
                        print(f"AI Response: {ai_response.status_code}")

                        if ai_response.status_code == 201:
                            print("✓ تم إرسال الملف للتحليل بنجاح")
                            ai_sent = True
                            break
                    except Exception as e:
                        print(f"خطأ في الاتصال: {e}")

                if not ai_sent:
                    print("✗ فشل في إرسال الملف للتحليل")

            else:
                print(f"✗ فشل في رفع الملف: {artifact_response.status_code}")
                print(f"Response: {artifact_response.text}")

        else:
            print(f"✗ فشل في إنشاء المشروع: {project_response.status_code}")
            print(f"Response: {project_response.text}")

    else:
        print(f"✗ فشل في تسجيل الدخول: {login_response.status_code}")
        print(f"Response: {login_response.text}")

except Exception as e:
    print(f"خطأ في الاختبار: {e}")

print("\n=== انتهى الاختبار البسيط ===")
