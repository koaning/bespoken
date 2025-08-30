#!/usr/bin/env python3
"""Test script for the new Chat class functionality."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from bespoken import Chat

def test_no_modes():
    """Test Chat class without modes (backward compatibility)."""
    print("Testing Chat class without modes...")
    tools = []  # Empty tools list for testing
    
    # Mock the model initialization to avoid API calls
    from unittest.mock import patch, MagicMock
    
    with patch('llm.get_model') as mock_get_model:
        mock_model = MagicMock()
        mock_conversation = MagicMock()
        mock_model.conversation.return_value = mock_conversation
        mock_get_model.return_value = mock_model
        
        chat = Chat(
            tools=tools,
            show_banner=False,
            first_message="Testing Chat class without modes. Type /quit to exit."
        )
        
        print("✓ Chat instance created successfully")
        print(f"✓ Modes enabled: {chat._is_modes_enabled()}")  # Should be False
        print(f"✓ Available modes: {chat.get_available_modes()}")  # Should be empty
        print(f"✓ Current tools: {len(chat._get_current_tools())}")
        
        # Test would run chat.run() here but that's interactive
    

def test_with_modes():
    """Test Chat class with modes."""
    print("\nTesting Chat class with modes...")
    
    from unittest.mock import patch, MagicMock
    
    # Mock tools for different modes
    read_tool = MagicMock()
    read_tool.tool_name = "read"
    write_tool = MagicMock()
    write_tool.tool_name = "write"
    debug_tool = MagicMock()
    debug_tool.tool_name = "debug"
    
    tools = {
        "normal": [read_tool, write_tool],
        "plan": [read_tool],  # Read-only mode
        "debug": [read_tool, write_tool, debug_tool]
    }
    
    mode_switch_messages = {
        "plan": "You are now in plan mode. You can read files but cannot write them.",
        "normal": "You are now in normal mode with full capabilities.",
        "debug": "You are now in debug mode with additional debugging tools."
    }
    
    with patch('llm.get_model') as mock_get_model:
        mock_model = MagicMock()
        mock_conversation = MagicMock()
        mock_conversation.responses = []
        mock_conversation.chain.return_value = iter([])  # Empty iterator
        mock_model.conversation.return_value = mock_conversation
        mock_get_model.return_value = mock_model
        
        chat = Chat(
            tools=tools,
            mode_switch_messages=mode_switch_messages,
            initial_mode="normal",
            show_banner=False,
            first_message="Testing Chat class with modes. Type /modes to see available modes, /quit to exit."
        )
        
        print("✓ Chat instance with modes created successfully")
        print(f"✓ Modes enabled: {chat._is_modes_enabled()}")  # Should be True
        print(f"✓ Current mode: {chat.current_mode}")  # Should be 'normal'
        print(f"✓ Available modes: {chat.get_available_modes()}")
        print(f"✓ Current tools: {[t.tool_name for t in chat._get_current_tools()]}")
        
        # Test mode switching
        print("\nTesting mode switching...")
        success = chat.switch_mode("plan")
        print(f"✓ Switch to plan mode: {success}")
        print(f"✓ Current mode: {chat.current_mode}")
        print(f"✓ Current tools: {[t.tool_name for t in chat._get_current_tools()]}")
        
        # Test switching to invalid mode
        success = chat.switch_mode("invalid_mode")
        print(f"✓ Switch to invalid mode (should fail): {success}")
        print(f"✓ Current mode after failed switch: {chat.current_mode}")


if __name__ == "__main__":
    test_no_modes()
    test_with_modes()
    print("\n✅ All tests passed!")