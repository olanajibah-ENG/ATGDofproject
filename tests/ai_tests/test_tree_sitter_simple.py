#!/usr/bin/env python3
"""
Simple test script to verify Tree-sitter Java language loading with tree-sitter-languages
"""
import sys

def test_tree_sitter():
    try:
        print("Testing Tree-sitter imports...")
        import tree_sitter

        print("✓ tree_sitter imported successfully")

        # Try tree-sitter-languages first
        try:
            from tree_sitter_languages import get_language
            print("✓ tree_sitter_languages available")

            try:
                java_lang = get_language('java')
                print("✓ Java language loaded from tree_sitter_languages")

                parser = tree_sitter.Parser()
                parser.set_language(java_lang)

                # Test parsing simple Java code
                test_code = "public class Test { }"
                tree = parser.parse(test_code.encode('utf-8'))

                if tree:
                    print("✓ Successfully parsed Java code")
                    print(f"Root node type: {tree.root_node.type}")
                else:
                    print("✗ Failed to parse Java code")

            except Exception as e:
                print(f"✗ Failed to load Java from tree_sitter_languages: {e}")

        except ImportError:
            print("tree_sitter_languages not available, trying direct import...")

            # Fallback to tree-sitter-java
            try:
                import tree_sitter_java
                print("✓ tree_sitter_java available")

                java_lang = tree_sitter_java.language()
                print("✓ Java language loaded from tree_sitter_java")

                parser = tree_sitter.Parser()
                parser.set_language(java_lang)

                # Test parsing
                test_code = "public class Test { }"
                tree = parser.parse(test_code.encode('utf-8'))

                if tree:
                    print("✓ Successfully parsed Java code")
                    print(f"Root node type: {tree.root_node.type}")
                else:
                    print("✗ Failed to parse Java code")

            except ImportError:
                print("✗ Neither tree_sitter_languages nor tree_sitter_java available")
                return False

        return True

    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_tree_sitter()
    print(f"\nTest {'PASSED' if success else 'FAILED'}")
    sys.exit(0 if success else 1)
