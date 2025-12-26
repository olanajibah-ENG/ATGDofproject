#!/usr/bin/env python3
"""
Simple test script for Java processor
"""
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'Ai_project'))

from core_ai.language_processors.java_processor import JavaProcessor

def test_java_simple():
    print("Testing Java processor with simple code...")

    # Create processor
    processor = JavaProcessor()

    # Simple Java code
    java_code = '''
public class SimpleTest {
    private String name;
    private int age;

    public SimpleTest(String name, int age) {
        this.name = name;
        this.age = age;
    }

    public void display() {
        System.out.println("Name: " + name + ", Age: " + age);
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }
}
'''

    # Test parsing
    print("1. Testing code parsing...")
    ast_result = processor.parse_source_code(java_code)

    if ast_result.get("error"):
        print(f"❌ Parse failed: {ast_result['error']}")
        return False

    print("✅ Code parsed successfully")

    # Test feature extraction
    print("2. Testing feature extraction...")
    features = processor.extract_features(ast_result)
    print(f"   Lines of code: {features.get('lines_of_code', 0)}")
    print(f"   Methods: {features.get('methods', 0)}")

    # Test semantic analysis
    print("3. Testing semantic analysis...")
    semantic = processor.perform_semantic_analysis(ast_result, features)
    issues = semantic.get('issues', [])
    print(f"   Found {len(issues)} issues")

    # Test class diagram generation
    print("4. Testing class diagram generation...")
    class_diagram = processor.generate_class_diagram_data(ast_result, features)

    classes = class_diagram.get('classes', [])
    print(f"   Found {len(classes)} classes")

    for cls in classes:
        print(f"   - Class: {cls['name']}")
        print(f"     Methods: {len(cls.get('methods', []))}")
        print(f"     Attributes: {len(cls.get('attributes', []))}")
        print(f"     Associations: {len(cls.get('associations', []))}")

        if cls.get('associations'):
            for assoc in cls['associations']:
                print(f"     → {assoc['type']} {assoc['target_class']}")

    print("✅ All tests passed!")
    return True

if __name__ == "__main__":
    success = test_java_simple()
    print(f"\nTest result: {'PASSED' if success else 'FAILED'}")
    sys.exit(0 if success else 1)
