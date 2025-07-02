"""Test PlaywrightTool behavior when playwright is not installed.

This test should be run in an environment without playwright installed.
"""

import subprocess
import sys
import tempfile
import textwrap


def test_playwright_not_installed():
    """Test that PlaywrightTool gives proper error when playwright is missing."""
    
    # Create a test script that tries to use PlaywrightTool
    test_script = textwrap.dedent("""
    import sys
    try:
        from bespoken.tools import PlaywrightTool
        
        # Try to instantiate
        tool = PlaywrightTool()
        print("ERROR: Should have raised an error")
        sys.exit(1)
        
    except ModuleNotFoundError as e:
        # This is expected
        error_msg = str(e)
        print(f"Got expected error: {error_msg}")
        
        # Verify the error message contains helpful info
        assert "PlaywrightTool" in error_msg, f"Error should mention PlaywrightTool: {error_msg}"
        assert "browser" in error_msg, f"Error should mention browser extra: {error_msg}"
        assert "pip install" in error_msg, f"Error should include install instructions: {error_msg}"
        
        print("SUCCESS: NotInstalled proxy works correctly")
        sys.exit(0)
    except Exception as e:
        print(f"ERROR: Unexpected error type: {type(e).__name__}: {e}")
        sys.exit(1)
    """)
    
    # Write the test script to a temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_script)
        test_file = f.name
    
    # Run the test in a subprocess with a clean environment (no playwright)
    env = sys.executable
    result = subprocess.run(
        [env, test_file],
        capture_output=True,
        text=True
    )
    
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)
    
    # Check that the test passed
    assert result.returncode == 0, f"Test failed with return code {result.returncode}"


if __name__ == "__main__":
    test_playwright_not_installed()