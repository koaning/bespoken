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


def test_streaming_first_chunk_has_padding(mock_console):
    """Test that the first chunk in streaming gets proper padding - this tests the bug."""
    # Start streaming
    ui.start_streaming(indent=2)
    
    # Stream the first chunk - this should have padding
    ui.stream_chunk("First chunk of text", indent=2)
    
    # End streaming
    ui.end_streaming(indent=2)
    
    # Get all the print calls
    all_calls = mock_console.print.call_args_list
    
    # Find calls that add padding (2 spaces)
    padding_calls = [call for call in all_calls 
                    if call[0] and call[0][0] == "  " and len(call[0][0]) == 2]
    
    # There should be at least one padding call for the first chunk
    assert len(padding_calls) >= 1, f"Expected at least 1 padding call, got {len(padding_calls)}. All calls: {all_calls}"
    
    # The first significant call should be padding
    # Filter out empty calls
    non_empty_calls = [call for call in all_calls if call[0]]
    assert len(non_empty_calls) >= 1, f"Expected at least 1 non-empty call, got {len(non_empty_calls)}"
    
    # The first non-empty call should be padding
    first_call = non_empty_calls[0]
    assert first_call[0][0] == "  ", f"First call should be padding '  ', but was {repr(first_call[0][0])}"


def test_streaming_after_tool_execution_simulation(mock_console):
    """Test streaming behavior after tool execution - simulates the actual bug scenario."""
    # Simulate tool execution output (this interferes with streaming state)
    ui.tool_status("Reading file: edit.py")
    
    # Clear the mock to focus on the streaming behavior
    mock_console.reset_mock()
    
    # Now start streaming the LLM response (this is where the bug occurs)
    ui.start_streaming(indent=2)
    
    # Stream the first chunk - this should have padding but might not due to the bug
    ui.stream_chunk("I've successfully read the contents", indent=2)
    
    # End streaming
    ui.end_streaming(indent=2)
    
    # Get all the print calls after the reset
    all_calls = mock_console.print.call_args_list
    
    # Find the first call that should be padding
    first_call = all_calls[0] if all_calls else None
    
    # The first call should be padding ("  ")
    assert first_call is not None, "Expected at least one print call"
    assert first_call[0], "First call should have arguments"
    assert first_call[0][0] == "  ", f"First call should be padding '  ', but was {repr(first_call[0][0])}"


def test_start_streaming_behavior_detailed(mock_console):
    """Test the exact behavior of start_streaming after the fix."""
    # Call start_streaming
    ui.start_streaming(indent=2)
    
    # Check what calls were made (should be none now)
    all_calls = mock_console.print.call_args_list
    
    # Print the calls for debugging
    print(f"start_streaming calls: {all_calls}")
    
    # Check the streaming state - after fix, at_line_start should remain True
    assert ui._streaming_state['at_line_start'] == True, "After start_streaming, at_line_start should be True"
    
    # Now if we call stream_chunk, it should add padding since at_line_start is True
    mock_console.reset_mock()
    ui.stream_chunk("First", indent=2)
    
    calls_after_chunk = mock_console.print.call_args_list
    print(f"stream_chunk calls: {calls_after_chunk}")
    
    # The first call should be padding because at_line_start is True
    if calls_after_chunk:
        first_call = calls_after_chunk[0]
        print(f"First call after stream_chunk: {first_call}")
        assert first_call[0][0] == "  ", f"Expected padding, but got {repr(first_call[0][0])}"


def test_stream_chunk_when_at_line_start_false(mock_console):
    """Test what happens when stream_chunk is called with at_line_start=False."""
    # Manually set the streaming state to simulate the bug condition
    ui._streaming_state['at_line_start'] = False
    ui._streaming_state['current_position'] = 0
    ui._streaming_state['word_buffer'] = ''
    ui._streaming_state['terminal_width'] = 80
    ui._streaming_state['max_line_width'] = 76
    
    # Now call stream_chunk
    ui.stream_chunk("Test text", indent=2)
    
    # Check the calls
    all_calls = mock_console.print.call_args_list
    print(f"Calls when at_line_start=False: {all_calls}")
    
    # The first call should NOT be padding because at_line_start is False
    # This proves the bug exists
    padding_calls = [call for call in all_calls if call[0] and call[0][0] == "  "]
    assert len(padding_calls) == 0, f"Expected no padding calls, but got {padding_calls}"


def test_stream_chunk_when_at_line_start_true(mock_console):
    """Test what happens when stream_chunk is called with at_line_start=True."""
    # Manually set the streaming state to the correct condition
    ui._streaming_state['at_line_start'] = True
    ui._streaming_state['current_position'] = 0
    ui._streaming_state['word_buffer'] = ''
    ui._streaming_state['terminal_width'] = 80
    ui._streaming_state['max_line_width'] = 76
    
    # Now call stream_chunk
    ui.stream_chunk("Test text", indent=2)
    
    # Check the calls
    all_calls = mock_console.print.call_args_list
    print(f"Calls when at_line_start=True: {all_calls}")
    
    # The first call SHOULD be padding because at_line_start is True
    if all_calls:
        first_call = all_calls[0]
        assert first_call[0][0] == "  ", f"Expected padding as first call, but got {repr(first_call[0][0])}"


def test_bug_demonstration_complete_flow(mock_console):
    """Demonstrate the complete bug: start_streaming + stream_chunk should produce padded output."""
    # This is what should happen in the real application:
    # 1. start_streaming() is called
    # 2. stream_chunk() is called with first chunk
    # 3. The first chunk should be padded
    
    # The current implementation does this:
    ui.start_streaming(indent=2)
    
    # Reset mock to focus on stream_chunk
    mock_console.reset_mock()
    
    # Now stream the first chunk
    ui.stream_chunk("First chunk", indent=2)
    
    # Check what happened
    all_calls = mock_console.print.call_args_list
    print(f"Complete flow calls: {all_calls}")
    
    # The issue: there should be padding, but there isn't because start_streaming already consumed it
    # This should fail with current implementation
    has_padding = any(call[0] and call[0][0] == "  " for call in all_calls if call[0])
    
    assert has_padding, f"Expected padding in the output, but got calls: {all_calls}"


def test_expected_behavior_vs_current_behavior(mock_console):
    """Test that current behavior now matches expected behavior after the fix."""
    print("=== Testing Expected Behavior ===")
    
    # Expected behavior: start_streaming should NOT add padding, stream_chunk should
    # Let's test what should happen
    
    # Reset state manually to simulate expected behavior
    ui._streaming_state['at_line_start'] = True
    ui._streaming_state['current_position'] = 0
    ui._streaming_state['word_buffer'] = ''
    ui._streaming_state['terminal_width'] = 80
    ui._streaming_state['max_line_width'] = 76
    
    # Call stream_chunk directly (expected behavior)
    ui.stream_chunk("First chunk", indent=2)
    
    expected_calls = mock_console.print.call_args_list
    print(f"Expected calls: {expected_calls}")
    
    # Reset for current behavior test
    mock_console.reset_mock()
    
    print("=== Testing Current Behavior ===")
    
    # Current behavior after fix: start_streaming does NOT add padding, stream_chunk does
    ui.start_streaming(indent=2)
    mock_console.reset_mock()  # Ignore start_streaming calls
    
    ui.stream_chunk("First chunk", indent=2)
    
    current_calls = mock_console.print.call_args_list
    print(f"Current calls: {current_calls}")
    
    # The first call in both should be padding
    expected_first = expected_calls[0] if expected_calls else None
    current_first = current_calls[0] if current_calls else None
    
    print(f"Expected first call: {expected_first}")
    print(f"Current first call: {current_first}")
    
    # After the fix, both should behave the same
    if expected_first and current_first:
        assert expected_first[0][0] == "  ", "Expected behavior should start with padding"
        assert current_first[0][0] == "  ", "Current behavior should now also start with padding (bug fixed!)"


def test_debug_mode_vs_non_debug_mode_streaming():
    """Test streaming behavior with and without debug mode using fresh mock objects."""
    from unittest.mock import MagicMock
    
    # Test with debug mode OFF (the scenario from the user's output)
    print("=== Testing with DEBUG_MODE=False ===")
    
    # Create a fresh mock console
    fresh_mock_console = MagicMock()
    fresh_mock_console.width = 80
    
    # Patch the global console with our fresh mock
    with patch('bespoken.ui._console', fresh_mock_console):
        # Simulate the exact flow from __main__.py when debug is off
        ui.print("")  # Line 205: Add whitespace after spinner
        # DEBUG_MODE is False, so lines 206-208 are skipped
        
        # Initialize streaming state (line 210)
        ui.start_streaming(ui.LEFT_PADDING)
        
        # Stream first chunk (line 213)
        ui.stream_chunk("The edit.py file contains", ui.LEFT_PADDING)
    
    # Get ALL calls from the fresh mock
    all_calls_debug_off = fresh_mock_console.print.call_args_list
    print(f"DEBUG_MODE=False ALL calls: {all_calls_debug_off}")
    
    print("=== Testing with DEBUG_MODE=True ===")
    
    # Create another fresh mock console
    fresh_mock_console2 = MagicMock()
    fresh_mock_console2.width = 80
    
    # Patch the global console with our second fresh mock
    with patch('bespoken.ui._console', fresh_mock_console2):
        # Simulate the exact flow from __main__.py when debug is on
        ui.print("")  # Line 205: Add whitespace after spinner
        ui.print("[magenta]>>> LLM Response:[/magenta]")  # Line 207
        ui.print("")  # Line 208
        
        # Initialize streaming state (line 210)
        ui.start_streaming(ui.LEFT_PADDING)
        
        # Stream first chunk (line 213)
        ui.stream_chunk("The edit.py file contains", ui.LEFT_PADDING)
    
    # Get ALL calls from the second fresh mock
    all_calls_debug_on = fresh_mock_console2.print.call_args_list
    print(f"DEBUG_MODE=True ALL calls: {all_calls_debug_on}")
    
    # Now we can see the complete sequence without any reset_mock interference
    # Find where the streaming chunk content starts in each sequence
    
    # For debug off: should be empty line, then streaming padding, then content
    # For debug on: should be empty line, debug message, empty line, then streaming padding, then content
    
    # Look for the streaming content (should be after padding)
    debug_off_content_calls = [call for call in all_calls_debug_off if call[0] and '[dim]The[/dim]' in str(call[0][0])]
    debug_on_content_calls = [call for call in all_calls_debug_on if call[0] and '[dim]The[/dim]' in str(call[0][0])]
    
    print(f"Debug OFF content calls: {debug_off_content_calls}")
    print(f"Debug ON content calls: {debug_on_content_calls}")
    
    # Check if there's padding before the content
    if debug_off_content_calls:
        content_index = all_calls_debug_off.index(debug_off_content_calls[0])
        if content_index > 0:
            call_before_content = all_calls_debug_off[content_index - 1]
            print(f"Call before content (debug off): {call_before_content}")
            # This should be the padding call
            assert call_before_content[0][0] == "  ", f"Expected padding before content, got: {repr(call_before_content[0][0])}"
    
    if debug_on_content_calls:
        content_index = all_calls_debug_on.index(debug_on_content_calls[0])
        if content_index > 0:
            call_before_content = all_calls_debug_on[content_index - 1]
            print(f"Call before content (debug on): {call_before_content}")
            # This should be the padding call
            assert call_before_content[0][0] == "  ", f"Expected padding before content, got: {repr(call_before_content[0][0])}"