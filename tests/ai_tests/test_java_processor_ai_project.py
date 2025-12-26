#!/usr/bin/env python3
"""
Test script to verify Java processor functionality
"""
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core_ai.language_processors.java_processor import JavaProcessor

def test_java_processor():
    try:
        print("Testing Java processor initialization...")
        processor = JavaProcessor()

        if processor._java_language is None or processor._internal_java_parser is None:
            print("✗ Java processor initialization failed")
            return False

        print("✓ Java processor initialized successfully")

        # Test parsing
        test_java_code = """
public class HelloWorld {
    private String message;

    public HelloWorld(String message) {
        this.message = message;
    }

    public void greet() {
        System.out.println(message);
    }

    public static void main(String[] args) {
        HelloWorld hello = new HelloWorld("Hello, World!");
        hello.greet();
    }
}
"""

        print("Testing Java code parsing...")
        ast_result = processor.parse_source_code(test_java_code)

        if ast_result.get("error"):
            print(f"✗ Parsing failed: {ast_result['error']}")
            return False

        print("✓ Java code parsed successfully")

        # Test feature extraction
        print("Testing feature extraction...")
        features = processor.extract_features(ast_result)
        print(f"✓ Features extracted: {features}")

        # Test semantic analysis
        print("Testing semantic analysis...")
        semantic = processor.perform_semantic_analysis(ast_result, features)
        print(f"✓ Semantic analysis completed: {semantic}")

        # Test class diagram generation
        print("Testing class diagram generation...")
        class_diagram = processor.generate_class_diagram_data(ast_result, features)
        print(f"✓ Class diagram generated: {len(class_diagram.get('classes', []))} classes found")

        return True

    except Exception as e:
        print(f"✗ Java processor test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_java_processor()
    sys.exit(0 if success else 1)
