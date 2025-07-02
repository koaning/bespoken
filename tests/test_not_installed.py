"""Test the NotInstalled proxy behavior."""

import pytest

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