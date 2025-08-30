#!/usr/bin/env python3
"""Test the mode UI picker functionality."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from unittest.mock import patch, MagicMock
from bespoken import Chat

def test_mode_ui_picker():
    """Test that the mode picker UI works correctly."""
    print("Testing mode UI picker...")
    
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
        
        # Test the mode command handler with mock choice
        with patch('src.bespoken.ui.choice') as mock_choice:
            # Test selecting a different mode
            mock_choice.return_value = "review"
            result = chat._handle_mode_command("")
            print(f"✓ Mode command handler returned: {result}")
            
            # Test the choices that would be presented
            expected_choices = ["development (current)", "review", "planning"]
            mock_choice.assert_called_with("Select mode:", expected_choices)
            print(f"✓ Choice UI called with correct options")
            
        print("✓ Mode UI picker functionality works correctly!")

if __name__ == "__main__":
    test_mode_ui_picker()
    print("\n✅ All mode UI tests passed!")