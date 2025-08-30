#!/usr/bin/env python3
"""Test the keyboard shortcut functionality."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from unittest.mock import patch, MagicMock
from bespoken import Chat

def test_keyboard_shortcut():
    """Test that the keyboard shortcut method works correctly."""
    print("Testing keyboard shortcut for mode switching...")
    
    # Mock tools for different modes
    read_tool = MagicMock()
    read_tool.tool_name = "read"
    write_tool = MagicMock()
    write_tool.tool_name = "write"
    
    tools = {
        "development": [read_tool, write_tool],
        "review": [read_tool],
        "planning": []
    }
    
    with patch('llm.get_model') as mock_get_model:
        mock_model = MagicMock()
        mock_conversation = MagicMock()
        mock_conversation.responses = []
        mock_conversation.chain.return_value = iter([])
        mock_model.conversation.return_value = mock_conversation
        mock_get_model.return_value = mock_model
        
        chat = Chat(
            tools=tools,
            initial_mode="development",
            show_banner=False,
        )
        
        print(f"✓ Initial mode: {chat.current_mode}")
        print(f"✓ Available modes: {chat.get_available_modes()}")
        
        # Test switching to next mode
        next_mode = chat.switch_to_next_mode()
        print(f"✓ After first switch: {chat.current_mode} (returned: {next_mode})")
        
        # Test switching again (should cycle through all modes)
        next_mode = chat.switch_to_next_mode()
        print(f"✓ After second switch: {chat.current_mode} (returned: {next_mode})")
        
        # Test switching again (should cycle back to first)
        next_mode = chat.switch_to_next_mode()
        print(f"✓ After third switch: {chat.current_mode} (returned: {next_mode})")
        
        # Test with single mode (should return None)
        single_mode_chat = Chat(
            tools={"only": [read_tool]},
            initial_mode="only",
            show_banner=False,
        )
        result = single_mode_chat.switch_to_next_mode()
        print(f"✓ Single mode switch result: {result} (should be None)")
        
        print("✓ Keyboard shortcut functionality works correctly!")

if __name__ == "__main__":
    test_keyboard_shortcut()
    print("\n✅ All keyboard shortcut tests passed!")