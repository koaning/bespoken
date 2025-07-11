"""Tests for file tools - focusing on the edit/replace functionality."""

import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch
import pytest

from bespoken.tools import FileSystem
from bespoken import config


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    temp_path = tempfile.mkdtemp()
    yield Path(temp_path)
    shutil.rmtree(temp_path)


@pytest.fixture
def file_tools(temp_dir):
    """Create FileSystem instance with temporary directory."""
    return FileSystem(str(temp_dir))


@pytest.fixture(autouse=True)
def reset_debug_mode():
    """Reset debug mode after each test."""
    original = config.DEBUG_MODE
    yield
    config.DEBUG_MODE = original


@patch('rich.prompt.Confirm.ask')
@patch('builtins.print')
def test_replace_in_file_accepted(mock_print, mock_confirm, file_tools, temp_dir):
    """Test replacing text in file when user accepts."""
    test_file = temp_dir / "test.txt"
    test_file.write_text("Hello, World!")
    
    mock_confirm.return_value = True
    
    result = file_tools.replace_in_file("test.txt", "World", "Python")
    
    assert result == "Applied changes to 'test.txt'"
    assert test_file.read_text() == "Hello, Python!"
    assert mock_confirm.called


@patch('rich.prompt.Confirm.ask')
@patch('builtins.print')
def test_replace_in_file_declined(mock_print, mock_confirm, file_tools, temp_dir):
    """Test replacing text in file when user declines."""
    test_file = temp_dir / "test.txt"
    original_content = "Hello, World!"
    test_file.write_text(original_content)
    
    mock_confirm.return_value = False
    
    result = file_tools.replace_in_file("test.txt", "World", "Python")
    
    assert "user declined" in result
    assert test_file.read_text() == original_content  # Content unchanged
    assert mock_confirm.called


@patch('builtins.print')
def test_replace_in_file_no_changes(mock_print, file_tools, temp_dir):
    """Test replacing text when no matches found."""
    test_file = temp_dir / "test.txt"
    test_file.write_text("Hello, World!")
    
    result = file_tools.replace_in_file("test.txt", "Python", "Java")
    
    assert result == "No changes needed in 'test.txt'"


@patch('rich.prompt.Confirm.ask')
@patch('builtins.print')
def test_replace_in_file_multiple_occurrences(mock_print, mock_confirm, file_tools, temp_dir):
    """Test replacing multiple occurrences of text."""
    test_file = temp_dir / "test.txt"
    test_file.write_text("Hello, World! Welcome to the World of Python.")
    
    mock_confirm.return_value = True
    
    result = file_tools.replace_in_file("test.txt", "World", "Universe")
    
    assert result == "Applied changes to 'test.txt'"
    assert test_file.read_text() == "Hello, Universe! Welcome to the Universe of Python."


@patch('bespoken.ui.tool_debug')
@patch('bespoken.ui.tool_status')
def test_replace_in_file_with_debug_mode(mock_tool_status, mock_tool_debug, file_tools, temp_dir):
    """Test that debug mode shows appropriate messages during replace."""
    config.DEBUG_MODE = True
    test_file = temp_dir / "test.txt"
    test_file.write_text("Hello, World!")
    
    file_tools.replace_in_file("test.txt", "Python", "Java")
    
    # Check that debug messages were called
    debug_calls = [str(call[0][0]) for call in mock_tool_debug.call_args_list]
    assert any("LLM calling tool: replace_in_file(" in msg for msg in debug_calls)
    assert any("Tool returning to LLM" in msg for msg in debug_calls)