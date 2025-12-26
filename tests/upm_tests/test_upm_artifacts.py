import requests
import json

# Test UPM API Authentication and Artifacts Upload
BASE_URL = "http://localhost:8001/api/upm"

def test_upm_api():
    print("=== UPM API Test ===")

    # Step 1: Try to login with existing user or register new user
    print("\n1. User Authentication...")

    # Try to register a new user
    register_data = {
        "username": "testuser_api",
        "email": "testuser_api@example.com",
        "password": "testpass123"
    }

    try:
        register_response = requests.post(f"{BASE_URL}/auth/register/", json=register_data)
        print(f"Register Response: {register_response.status_code}")

        if register_response.status_code == 201:
            print("✓ User registered successfully")
            user_data = register_response.json()
        elif register_response.status_code == 400:
            print("User might already exist, trying to login...")
            # Try to login instead
            login_data = {
                "username": "testuser_api",
                "password": "testpass123"
            }
            login_response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
            print(f"Login Response: {login_response.status_code}")

            if login_response.status_code == 200:
                print("✓ User logged in successfully")
                user_data = login_response.json()
            else:
                print(f"✗ Login failed: {login_response.status_code}")
                print(f"Response: {login_response.text}")
                return
        else:
            print(f"✗ Register failed: {register_response.status_code}")
            print(f"Response: {register_response.text}")
            return

        # Extract token
        token = user_data.get('access')
        if not token:
            print("✗ No access token received")
            return

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        print(f"✓ Token obtained: {token[:20]}...")

        # Step 2: Create a project
        print("\n2. Creating Project...")
        project_data = {
            "name": "Test API Project",
            "description": "Project created via API test"
        }

        project_response = requests.post(f"{BASE_URL}/projects/", json=project_data, headers=headers)
        print(f"Create Project Response: {project_response.status_code}")

        if project_response.status_code == 201:
            project = project_response.json()
            project_id = project.get('id')
            print(f"✓ Project created: {project_id}")

            # Step 3: Upload an artifact
            print("\n3. Uploading Artifact...")

            # First, create an artifact record
            artifact_data = {
                "project_id": project_id,
                "name": "Test Artifact API",
                "description": "Artifact uploaded via API test",
                "artifact_type": "code",
                "content": "print('Hello from API test')",
                "file_type": "python"
            }

            artifact_response = requests.post(f"{BASE_URL}/artifacts/", json=artifact_data, headers=headers)
            print(f"Create Artifact Response: {artifact_response.status_code}")

            if artifact_response.status_code == 201:
                artifact = artifact_response.json()
                artifact_id = artifact.get('id')
                print(f"✓ Artifact created: {artifact_id}")

                # Step 4: Try to send artifact to AI analysis
                print("\n4. Sending to AI Analysis...")

                ai_payload = {
                    "artifact_id": artifact_id,
                    "content": artifact_data["content"],
                    "file_type": artifact_data["file_type"],
                    "filename": f"artifact_{artifact_id}.py"
                }

                # Try different AI endpoints
                ai_endpoints = [
                    "http://localhost:8002/api/analysis/codefiles/",
                    "http://ai_web:8000/api/analysis/codefiles/"
                ]

                ai_success = False
                for ai_url in ai_endpoints:
                    try:
                        print(f"Trying AI endpoint: {ai_url}")
                        ai_response = requests.post(ai_url, json=ai_payload, timeout=10)
                        print(f"AI Response: {ai_response.status_code}")

                        if ai_response.status_code == 201:
                            ai_result = ai_response.json()
                            print(f"✓ AI analysis started: {ai_result.get('id')}")
                            ai_success = True
                            break
                        else:
                            print(f"AI endpoint failed: {ai_response.status_code}")
                    except Exception as e:
                        print(f"AI endpoint error: {e}")

                if not ai_success:
                    print("✗ All AI endpoints failed")

                # Step 5: Get project artifacts
                print("\n5. Getting Project Artifacts...")
                artifacts_response = requests.get(f"{BASE_URL}/projects/{project_id}/artifacts/", headers=headers)
                print(f"Get Artifacts Response: {artifacts_response.status_code}")

                if artifacts_response.status_code == 200:
                    artifacts = artifacts_response.json()
                    print(f"✓ Found {len(artifacts)} artifacts in project")
                else:
                    print(f"✗ Failed to get artifacts: {artifacts_response.status_code}")

            else:
                print(f"✗ Artifact creation failed: {artifact_response.status_code}")
                print(f"Response: {artifact_response.text}")

        else:
            print(f"✗ Project creation failed: {project_response.status_code}")
            print(f"Response: {project_response.text}")

    except Exception as e:
        print(f"✗ Test failed with error: {e}")

    print("\n=== Test Completed ===")

if __name__ == "__main__":
    test_upm_api()
