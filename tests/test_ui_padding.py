"""Tests for UI printing functionality - ensuring proper padding and formatting."""

import pytest
from unittest.mock import patch, MagicMock, call
from bespoken import ui


@pytest.fixture
def mock_console():
    """Mock the Rich console."""
    with patch('bespoken.ui._console') as mock:
        # Set a reasonable terminal width for testing
        mock.width = 80
        yield mock


def test_print_single_line_with_padding(mock_console):
    """Test that single line print adds correct left padding."""
    ui.print("Hello, World!")
    
    mock_console.print.assert_called_once_with("  Hello, World!")


def test_print_multi_line_with_padding(mock_console):
    """Test that multi-line print adds padding to each line."""
    ui.print("Line 1\nLine 2\nLine 3")
    
    expected_calls = [
        call("  Line 1"),
        call("  Line 2"),
        call("  Line 3")
    ]
    mock_console.print.assert_has_calls(expected_calls)


def test_print_custom_indent(mock_console):
    """Test print with custom indentation."""
    ui.print("Custom indent", indent=4)
    
    mock_console.print.assert_called_once_with("    Custom indent")


def test_tool_status_with_padding(mock_console):
    """Test tool status message has correct padding and formatting."""
    ui.tool_status("Running test command")
    
    expected_calls = [
        call(),  # Empty line before
        call("  [cyan]Running test command[/cyan]"),
        call()   # Empty line after
    ]
    mock_console.print.assert_has_calls(expected_calls)


def test_tool_error_with_padding(mock_console):
    """Test error message has correct padding and color."""
    ui.tool_error("Something went wrong")
    
    mock_console.print.assert_called_once_with("  [red]Something went wrong[/red]")


def test_tool_success_with_padding(mock_console):
    """Test success message has correct padding and color."""
    ui.tool_success("Operation completed")
    
    mock_console.print.assert_called_once_with("  [green]Operation completed[/green]")


def test_tool_warning_with_padding(mock_console):
    """Test warning message has correct padding and color."""
    ui.tool_warning("This might be a problem")
    
    mock_console.print.assert_called_once_with("  [yellow]This might be a problem[/yellow]")


@patch('bespoken.config.DEBUG_MODE', True)
def test_tool_debug_with_padding(mock_console):
    """Test debug message has correct padding when debug mode is on."""
    ui.tool_debug("Debug information")
    
    mock_console.print.assert_called_once_with("  [magenta]Debug information[/magenta]")


@patch('bespoken.config.DEBUG_MODE', False)
def test_tool_debug_no_output_when_disabled(mock_console):
    """Test debug message doesn't print when debug mode is off."""
    ui.tool_debug("Debug information")
    
    mock_console.print.assert_not_called()


@patch('bespoken.config.DEBUG_MODE', True)
def test_tool_debug_multiline_with_padding(mock_console):
    """Test multiline debug messages have padding on each line."""
    ui.tool_debug("Line 1\nLine 2\nLine 3")
    
    expected_calls = [
        call("  [magenta]Line 1[/magenta]"),
        call("  [magenta]Line 2[/magenta]"),
        call("  [magenta]Line 3[/magenta]")
    ]
    mock_console.print.assert_has_calls(expected_calls)


def test_print_neutral_with_padding(mock_console):
    """Test print_neutral adds correct padding and formatting."""
    ui.print_neutral("Neutral text message")
    
    # print_neutral uses streaming, so we need to check the print calls
    # It should have padding and end with a newline
    assert mock_console.print.call_count >= 2  # At least padding and newline


def test_show_banner_with_padding(mock_console):
    """Test that banner lines have correct padding."""
    ui.show_banner()
    
    # Banner should be printed with join, check that it was called
    assert mock_console.print.call_count >= 1
    
    # Get the actual call argument
    banner_call = mock_console.print.call_args_list[-1]
    banner_text = banner_call[0][0] if banner_call[0] else ""
    
    # Check that each line in the banner has padding
    lines = banner_text.split('\n')
    # Skip empty lines and color tags
    content_lines = [line for line in lines if line.strip() and not line.strip().startswith('[')]
    
    # Each content line should start with padding (2 spaces)
    for line in content_lines:
        if line and not line.startswith('['):  # Skip markup lines
            assert line.startswith("  "), f"Line should start with 2 spaces: '{line}'"


def test_stream_chunk_word_wrapping(mock_console):
    """Test that streaming respects terminal width and adds padding."""
    # Set up streaming state
    ui.start_streaming(indent=2)
    
    # Create a long word that would exceed line width
    long_text = "This is a very long line that should wrap properly with correct padding maintained on each wrapped line"
    
    ui.stream_chunk(long_text, indent=2)
    ui.end_streaming(indent=2)
    
    # Should have multiple print calls due to wrapping
    assert mock_console.print.call_count > 1
    
    # Check that padding was added
    padding_calls = [call for call in mock_console.print.call_args_list 
                    if call[0] and call[0][0] == "  "]
    assert len(padding_calls) > 0


def test_stream_chunk_preserves_newlines(mock_console):
    """Test that streaming preserves newlines and adds padding after them."""
    ui.start_streaming(indent=2)
    ui.stream_chunk("Line 1\nLine 2\nLine 3", indent=2)
    ui.end_streaming(indent=2)
    
    # Should have newline calls
    newline_calls = [call for call in mock_console.print.call_args_list 
                    if call == call()]
    assert len(newline_calls) >= 2  # At least 2 newlines in the text


def test_confirm_with_padding():
    """Test that confirm prompt has correct padding."""
    with patch('rich.prompt.Confirm.ask') as mock_confirm:
        mock_confirm.return_value = True
        
        result = ui.confirm("Continue with operation?", indent=4)
        
        # Check that the prompt was padded
        mock_confirm.assert_called_once()
        prompt_arg = mock_confirm.call_args[0][0]
        assert prompt_arg == "    Continue with operation?"
        assert result is True


@patch('questionary.select')
def test_choice_with_padding(mock_select):
    """Test that choice prompt has correct padding."""
    mock_question = MagicMock()
    mock_question.ask.return_value = "Option 1"
    mock_select.return_value = mock_question
    
    result = ui.choice("Select an option:", ["Option 1", "Option 2"], indent=3)
    
    # Check that the prompt was padded
    mock_select.assert_called_once()
    prompt_arg = mock_select.call_args[0][0]
    assert prompt_arg == "   Select an option:"
    assert result == "Option 1"


def test_padding_constants():
    """Test that padding constants are set correctly."""
    assert ui.LEFT_PADDING == 2
    assert ui.RIGHT_PADDING == 2


def test_stream_function_with_generator(mock_console):
    """Test the main stream function with a generator."""
    def text_generator():
        yield "Hello "
        yield "streaming "
        yield "world!"
    
    ui.stream(text_generator(), indent=3)
    
    # Should have multiple print calls for padding and content
    assert mock_console.print.call_count > 0
    
    # Check that padding was applied
    padding_calls = [call for call in mock_console.print.call_args_list 
                    if call[0] and call[0][0] == "   "]  # 3 spaces for indent=3
    assert len(padding_calls) > 0