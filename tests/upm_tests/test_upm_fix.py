import requests
import json

# Test UPM API Fix for Artifacts Upload
BASE_URL = "http://localhost:8001/api/upm"

def test_upm_fix():
    print("=== UPM API Fix Test ===")

    # Step 1: Register/Login
    print("\n1. Authentication...")

    register_data = {
        "username": "testuser2",
        "email": "test2@example.com",
        "password": "testpass123"
    }

    try:
        register_response = requests.post(f"{BASE_URL}/auth/register/", json=register_data)
        print(f"Register Response: {register_response.status_code}")

        if register_response.status_code == 201:
            print("✓ User registered")
            user_data = register_response.json()
        elif register_response.status_code == 400:
            print("User exists, trying login...")
            login_data = {
                "username": "testuser2",
                "password": "testpass123"
            }
            login_response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
            print(f"Login Response: {login_response.status_code}")

            if login_response.status_code == 200:
                print("✓ User logged in")
                user_data = login_response.json()
            else:
                print(f"✗ Login failed: {login_response.status_code}")
                return
        else:
            print(f"✗ Auth failed: {register_response.status_code}")
            return

        token = user_data.get('access')
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        # Step 2: Create project
        print("\n2. Creating Project...")
        project_data = {
            "name": "Fix Test Project",
            "description": "Testing UPM API fixes"
        }

        project_response = requests.post(f"{BASE_URL}/projects/", json=project_data, headers=headers)
        print(f"Project Response: {project_response.status_code}")

        if project_response.status_code == 201:
            project = project_response.json()
            project_id = project.get('id')
            print(f"✓ Project created: {project_id}")

            # Step 3: Test different artifact creation methods
            print("\n3. Testing Artifact Creation...")

            # Method 1: Direct artifact creation
            print("Method 1: Direct creation...")
            artifact_data = {
                "project_id": project_id,
                "name": "Fix Test Artifact",
                "description": "Testing artifact creation fix",
                "artifact_type": "code",
                "content": "def test():\n    print('Hello from fix test')",
                "file_type": "python"
            }

            artifact_response = requests.post(f"{BASE_URL}/artifacts/", json=artifact_data, headers=headers)
            print(f"Artifact Response: {artifact_response.status_code}")

            if artifact_response.status_code == 201:
                artifact = artifact_response.json()
                print(f"✓ Artifact created: {artifact.get('id')}")

                # Step 4: Test AI integration
                print("\n4. Testing AI Integration...")

                ai_data = {
                    "content": artifact_data["content"],
                    "file_type": artifact_data["file_type"],
                    "filename": f"fix_test_{artifact.get('id')}.py",
                    "artifact_id": artifact.get('id'),
                    "project_id": project_id
                }

                ai_urls = [
                    "http://localhost:8002/api/analysis/codefiles/",
                    "http://ai_web:8000/api/analysis/codefiles/"
                ]

                for ai_url in ai_urls:
                    try:
                        print(f"Trying: {ai_url}")
                        ai_response = requests.post(ai_url, json=ai_data, timeout=10)
                        print(f"AI Response: {ai_response.status_code}")

                        if ai_response.status_code == 201:
                            ai_result = ai_response.json()
                            print(f"✓ AI analysis started: {ai_result.get('id')}")
                            break
                        else:
                            print(f"AI failed: {ai_response.text[:100]}")
                    except Exception as e:
                        print(f"AI error: {e}")

            else:
                print(f"✗ Artifact creation failed: {artifact_response.status_code}")
                print(f"Response: {artifact_response.text}")

        else:
            print(f"✗ Project creation failed: {project_response.status_code}")
            print(f"Response: {project_response.text}")

    except Exception as e:
        print(f"✗ Test error: {e}")

    print("\n=== Fix Test Completed ===")

if __name__ == "__main__":
    test_upm_fix()
