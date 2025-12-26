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

        # Check version in a safe way (some packages don't have __version__)
        try:
            # Try multiple ways to get version
            if hasattr(tree_sitter, '__version__'):
                version = tree_sitter.__version__
            else:
                # Try importlib.metadata (Python 3.8+) or pkg_resources
                try:
                    from importlib.metadata import version
                    version = version('tree-sitter')
                except ImportError:
                    try:
                        import pkg_resources
                        version = pkg_resources.get_distribution('tree-sitter').version
                    except:
                        version = 'unknown'
            print(f"✓ tree_sitter imported successfully (version: {version})")
        except Exception as e:
            print(f"✓ tree_sitter imported successfully (version check failed: {e})")

        # Test Java language import using tree-sitter-languages (unified interface)
        try:
            import tree_sitter_languages
            print("✓ tree_sitter_languages imported successfully")

            # Get Java language from unified interface - try different approaches
            try:
                java_lang = tree_sitter_languages.get_language('java')
                print("✓ Java language loaded successfully via get_language('java')")
            except TypeError as e:
                print(f"✗ Direct get_language('java') failed: {e}, trying alternative approaches...")
                # Try with different parameters or alternative methods
                try:
                    # Some versions might need additional parameters
                    java_lang = tree_sitter_languages.get_language('java', None)
                    print("✓ Java language loaded successfully via get_language('java', None)")
                except Exception as e2:
                    print(f"✗ Alternative get_language also failed: {e2}")
                    # Try to import tree_sitter_java directly as fallback
                    try:
                        import tree_sitter_java
                        java_lang = tree_sitter_java.language()
                        print("✓ Java language loaded successfully via direct tree_sitter_java import")
                    except ImportError:
                        print("✗ tree_sitter_java not available")
                        raise e  # Re-raise original error

            # Test parser creation
            from tree_sitter import Parser
            parser = Parser()
            parser.set_language(java_lang)
            print("✓ Parser created and language set successfully")

            # Test parsing simple Java code
            test_code = """
public class Test {
    public static void main(String[] args) {
        System.out.println("Hello World");
    }
}
"""
            tree = parser.parse(test_code.encode('utf-8'))
            print("✓ Java code parsed successfully")
            print(f"✓ Parse tree root type: {tree.root_node.type}")

            return True

        except ImportError as e:
            print(f"✗ Failed to import tree_sitter_java: {e}")
            return False
        except Exception as e:
            print(f"✗ Failed to load/setup Java language: {e}")
            traceback.print_exc()
            return False

    except ImportError as e:
        print(f"✗ Failed to import tree_sitter: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_tree_sitter()
    sys.exit(0 if success else 1)
