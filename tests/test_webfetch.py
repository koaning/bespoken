"""Tests for the WebFetchTool."""

from unittest.mock import patch, Mock
import pytest
import requests

from bespoken.tools import WebFetchTool
from bespoken import config


@pytest.fixture
def webfetch_tool():
    """Create WebFetchTool instance."""
    return WebFetchTool(timeout=10)


@pytest.fixture(autouse=True)
def reset_debug_mode():
    """Reset debug mode after each test."""
    original = config.DEBUG_MODE
    yield
    config.DEBUG_MODE = original


@patch('requests.Session.get')
def test_fetch_url_success(mock_get, webfetch_tool):
    """Test successful URL fetching and markdown conversion."""
    mock_response = Mock()
    mock_response.text = "<html><body><h1>Test Title</h1><p>Test content</p></body></html>"
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response
    
    result = webfetch_tool.fetch_url("https://example.com")
    
    assert "# Test Title" in result
    assert "Test content" in result
    assert mock_get.called_with("https://example.com", timeout=10)




@patch('requests.Session.get')
def test_fetch_url_error(mock_get, webfetch_tool):
    """Test error handling when fetching fails."""
    mock_get.side_effect = requests.RequestException("Connection error")
    
    result = webfetch_tool.fetch_url("https://example.com")
    
    assert "Error:" in result
    assert "Connection error" in result




@patch('requests.Session.get')
@patch('bespoken.config.tool_debug')
@patch('bespoken.config.tool_status')
def test_debug_mode_output(mock_tool_status, mock_tool_debug, mock_get, webfetch_tool):
    """Test that debug mode shows appropriate messages."""
    config.DEBUG_MODE = True
    mock_response = Mock()
    mock_response.text = "<html><body>Test</body></html>"
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response
    
    webfetch_tool.fetch_url("https://example.com")
    
    # Check that debug messages were called
    debug_calls = [str(call[0][0]) for call in mock_tool_debug.call_args_list]
    assert any("LLM calling tool: fetch_url(" in msg for msg in debug_calls)
    assert any("Tool returning to LLM" in msg for msg in debug_calls)