"""Tests for the PlaywrightTool."""

import sys
from unittest.mock import patch, Mock, MagicMock
import pytest

from bespoken import config

# Skip all tests if playwright is not installed
pytest.importorskip("playwright")

from bespoken.tools import PlaywrightTool


@pytest.fixture
def mock_playwright():
    """Mock playwright components."""
    with patch('bespoken.tools.playwright_browser.sync_playwright') as mock_sync:
        mock_page = MagicMock()
        mock_browser = MagicMock()
        mock_browser.new_page.return_value = mock_page
        
        mock_playwright_instance = MagicMock()
        mock_playwright_instance.chromium.launch.return_value = mock_browser
        
        mock_sync.return_value.start.return_value = mock_playwright_instance
        
        yield {
            'sync_playwright': mock_sync,
            'playwright': mock_playwright_instance,
            'browser': mock_browser,
            'page': mock_page
        }


@pytest.fixture
def playwright_tool(mock_playwright):
    """Create PlaywrightTool instance with mocked playwright."""
    return PlaywrightTool(headless=True)


@pytest.fixture(autouse=True)
def reset_debug_mode():
    """Reset debug mode after each test."""
    original = config.DEBUG_MODE
    yield
    config.DEBUG_MODE = original


def test_navigate(playwright_tool, mock_playwright):
    """Test navigating to a URL."""
    mock_page = mock_playwright['page']
    mock_page.title.return_value = "Test Page"
    
    result = playwright_tool.navigate("https://example.com")
    
    assert "Successfully navigated" in result
    assert "Test Page" in result
    mock_page.goto.assert_called_with("https://example.com", wait_until="networkidle")


def test_click_text(playwright_tool, mock_playwright):
    """Test clicking text."""
    mock_page = mock_playwright['page']
    mock_text_element = MagicMock()
    mock_page.get_by_text.return_value.first = mock_text_element
    
    result = playwright_tool.click_text("Submit")
    
    assert "Successfully clicked" in result
    assert "Submit" in result
    mock_page.get_by_text.assert_called_with("Submit")
    mock_text_element.click.assert_called()


def test_fill_field_by_label(playwright_tool, mock_playwright):
    """Test filling field by label."""
    mock_page = mock_playwright['page']
    mock_label_element = MagicMock()
    mock_page.get_by_label.return_value = mock_label_element
    
    result = playwright_tool.fill_field("Email Address", "test@example.com")
    
    assert "Successfully filled" in result
    assert "test@example.com" in result
    mock_page.get_by_label.assert_called_with("Email Address")
    mock_label_element.fill.assert_called_with("test@example.com")


def test_fill_field_by_placeholder(playwright_tool, mock_playwright):
    """Test filling field by placeholder when label fails."""
    mock_page = mock_playwright['page']
    mock_page.get_by_label.side_effect = Exception("Not found")
    mock_placeholder_element = MagicMock()
    mock_page.get_by_placeholder.return_value = mock_placeholder_element
    
    result = playwright_tool.fill_field("Enter your email", "test@example.com")
    
    assert "Successfully filled" in result
    mock_page.get_by_placeholder.assert_called_with("Enter your email")
    mock_placeholder_element.fill.assert_called_with("test@example.com")


def test_get_content(playwright_tool, mock_playwright):
    """Test getting page content."""
    mock_page = mock_playwright['page']
    mock_page.inner_text.return_value = "Page content here"
    
    result = playwright_tool.get_content()
    
    assert "Page content here" in result
    mock_page.inner_text.assert_called_with("body")


def test_get_content_truncated(playwright_tool, mock_playwright):
    """Test content truncation for large pages."""
    mock_page = mock_playwright['page']
    mock_page.inner_text.return_value = "x" * 60000
    
    result = playwright_tool.get_content()
    
    assert len(result) < 60000
    assert "truncated" in result


def test_screenshot(playwright_tool, mock_playwright):
    """Test taking a screenshot."""
    mock_page = mock_playwright['page']
    
    result = playwright_tool.screenshot("test.png")
    
    assert "Screenshot saved to: test.png" in result
    mock_page.screenshot.assert_called_with(path="test.png")


def test_wait_for_text(playwright_tool, mock_playwright):
    """Test waiting for text."""
    mock_page = mock_playwright['page']
    mock_text_element = MagicMock()
    mock_page.get_by_text.return_value = mock_text_element
    
    result = playwright_tool.wait_for_text("Loading complete", timeout=5000)
    
    assert "is now visible" in result
    mock_page.get_by_text.assert_called_with("Loading complete")
    mock_text_element.wait_for.assert_called_with(timeout=5000)


def test_close(playwright_tool, mock_playwright):
    """Test closing the browser."""
    # Ensure browser is started first
    playwright_tool.navigate("https://example.com")
    
    result = playwright_tool.close()
    
    assert "Browser closed successfully" in result
    mock_playwright['page'].close.assert_called()
    mock_playwright['browser'].close.assert_called()


@patch('bespoken.config.tool_debug')
def test_debug_mode(mock_tool_debug, playwright_tool, mock_playwright):
    """Test debug output in debug mode."""
    config.DEBUG_MODE = True
    mock_page = mock_playwright['page']
    mock_page.title.return_value = "Test"
    
    playwright_tool.navigate("https://example.com")
    
    debug_calls = [str(call[0][0]) for call in mock_tool_debug.call_args_list]
    assert any("LLM calling tool: navigate(" in msg for msg in debug_calls)