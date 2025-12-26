#!/usr/bin/env python3
"""
Test script to verify Tree-sitter Java language loading
"""
import sys
import traceback

def test_tree_sitter():
    try:
        print("Testing Tree-sitter imports...")
        import tree_sitter

        print("✓ tree_sitter imported successfully")

        # Test tree-sitter-languages
        try:
            from tree_sitter_languages import get_language
            print("✓ tree_sitter_languages available")

            try:
                java_lang = get_language('java')
                print("✓ Java language loaded from tree_sitter_languages")

                parser = tree_sitter.Parser()
                parser.set_language(java_lang)

                # Test parsing
                test_code = """
public class HelloWorld {
    private String message;

    public HelloWorld(String msg) {
        this.message = msg;
    }

    public void greet() {
        System.out.println(message);
    }
}
"""
                tree = parser.parse(test_code.encode('utf-8'))
                if tree:
                    print("✓ Successfully parsed Java code")
                    print(f"Root node: {tree.root_node.type}")

                    # Walk through some nodes
                    cursor = tree.walk()
                    print("First few nodes:")
                    for i in range(5):
                        print(f"  - {cursor.node.type}: '{cursor.node.text.decode('utf-8')[:30]}...'")
                        if not cursor.goto_first_child():
                            break

                else:
                    print("✗ Failed to parse Java code")

            except Exception as e:
                print(f"✗ Failed to load Java from tree_sitter_languages: {e}")

        except ImportError:
            print("tree_sitter_languages not available, trying tree_sitter_java...")

            # Try tree-sitter-java
            try:
                import tree_sitter_java
                print("✓ tree_sitter_java available")

                java_lang = tree_sitter_java.language()
                parser = tree_sitter.Parser()
                parser.set_language(java_lang)

                print("✓ Java language loaded from tree_sitter_java")

                # Test parsing
                test_code = "public class Test { }"
                tree = parser.parse(test_code.encode('utf-8'))

                if tree:
                    print("✓ Successfully parsed Java code with tree_sitter_java")
                    print(f"Root node: {tree.root_node.type}")
                else:
                    print("✗ Failed to parse Java code")

            except ImportError:
                print("✗ tree_sitter_java not available")

        # Test language loading and basic parsing
        print("\nTesting language loading...")

        # Try different ways to load Java language
        java_loaded = False

        # Method 1: tree_sitter_languages
        try:
            from tree_sitter_languages import get_language
            java_lang = get_language('java')
            parser = tree_sitter.Parser()
            parser.set_language(java_lang)
            java_loaded = True
            print("✓ Java loaded via tree_sitter_languages")
        except:
            pass

        # Method 2: tree_sitter_java
        if not java_loaded:
            try:
                import tree_sitter_java
                java_lang = tree_sitter_java.language()
                parser = tree_sitter.Parser()
                parser.set_language(java_lang)
                java_loaded = True
                print("✓ Java loaded via tree_sitter_java")
            except:
                pass

        if java_loaded:
            print("✓ Java language successfully loaded")
            return True
        else:
            print("✗ Failed to load Java language")
            return False

    except Exception as e:
        print(f"✗ Test failed with error: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_tree_sitter()
    print(f"\nTest result: {'PASSED' if success else 'FAILED'}")
    sys.exit(0 if success else 1)
