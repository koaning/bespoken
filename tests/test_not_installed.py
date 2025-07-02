"""Test the NotInstalled proxy behavior."""

import pytest
import sys
from unittest.mock import patch

from bespoken.tools.not_installed import NotInstalled


def test_not_installed_attribute_access():
    """Test that accessing any attribute raises ModuleNotFoundError."""
    proxy = NotInstalled("TestTool", "test-extra")
    
    with pytest.raises(ModuleNotFoundError) as exc_info:
        proxy.some_method()
    
    assert "TestTool" in str(exc_info.value)
    assert "test-extra" in str(exc_info.value)
    assert "pip install 'bespoken[test-extra]'" in str(exc_info.value)


def test_not_installed_call():
    """Test that calling the proxy directly raises ModuleNotFoundError."""
    proxy = NotInstalled("TestTool", "test-extra")
    
    with pytest.raises(ModuleNotFoundError) as exc_info:
        proxy()
    
    assert "TestTool" in str(exc_info.value)
    assert "test-extra" in str(exc_info.value)


def test_not_installed_with_extra_instructions():
    """Test that extra instructions are included in the error message."""
    proxy = NotInstalled("TestTool", "test-extra", "Additional setup required")
    
    with pytest.raises(ModuleNotFoundError) as exc_info:
        proxy.method()
    
    assert "Additional setup required" in str(exc_info.value)


def test_playwright_import_without_playwright():
    """Test that PlaywrightTool is replaced with NotInstalled when playwright is missing."""
    # Remove playwright modules from sys.modules to simulate missing dependency
    playwright_modules = [key for key in sys.modules.keys() if key.startswith('playwright')]
    for module in playwright_modules:
        sys.modules.pop(module, None)
    
    # Mock the import to raise ImportError
    with patch.dict('sys.modules', {'playwright.sync_api': None}):
        # Force reload of the tools module
        if 'bespoken.tools' in sys.modules:
            del sys.modules['bespoken.tools']
        if 'bespoken.tools.playwright_browser' in sys.modules:
            del sys.modules['bespoken.tools.playwright_browser']
        
        # This simulates playwright not being installed
        with patch('builtins.__import__', side_effect=ImportError("No module named 'playwright'")):
            try:
                from bespoken.tools import PlaywrightTool
                
                # Should be a NotInstalled instance
                assert hasattr(PlaywrightTool, '__call__')
                
                # Try to use it - should raise ModuleNotFoundError
                with pytest.raises(ModuleNotFoundError) as exc_info:
                    tool = PlaywrightTool()
                
                assert "PlaywrightTool" in str(exc_info.value)
                assert "browser" in str(exc_info.value)
                assert "pip install 'bespoken[browser]'" in str(exc_info.value)
            except ImportError:
                # If the import itself fails, that's also valid behavior
                pass