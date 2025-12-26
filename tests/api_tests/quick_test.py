import requests

# Quick test to verify everything works
BASE_URL = "http://localhost:8002/api/analysis"

# Create a simple Python file
code = """
class Test:
    def __init__(self):
        self.engine = Engine()

class Engine:
    def __init__(self):
        self.hp = 200
"""

data = {
    "filename": "quick_test.py",
    "file_type": "python",
    "content": code.strip()
}

print("Testing AI analysis API...")
try:
    response = requests.post(f"{BASE_URL}/codefiles/", json=data)
    print(f"Create file: {response.status_code}")

    if response.status_code == 201:
        result = response.json()
        codefile_id = result['id']
        print(f"Created file with ID: {codefile_id}")

        # Analyze
        analyze_resp = requests.post(f"{BASE_URL}/codefiles/{codefile_id}/analyze/")
        print(f"Analyze: {analyze_resp.status_code}")

        # Wait and get results
        import time
        time.sleep(2)

        results_resp = requests.get(f"{BASE_URL}/analysis-results/")
        if results_resp.status_code == 200:
            results = results_resp.json()
            print(f"Found {len(results)} analysis results")

            # Look for our result
            for result in results:
                if result.get('code_file_id') == codefile_id:
                    print("✅ Analysis completed successfully!")
                    if 'class_diagram_data' in result:
                        classes = result['class_diagram_data'].get('classes', [])
                        print(f"Found {len(classes)} classes in diagram")
                    break
        else:
            print(f"❌ Failed to get results: {results_resp.status_code}")

    else:
        print(f"❌ Failed to create file: {response.status_code}")
        print(response.text)

except Exception as e:
    print(f"❌ Error: {e}")

print("Quick test completed.")
