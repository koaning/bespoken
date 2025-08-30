#!/usr/bin/env python3
"""Test that app.py can import and create the Chat instance without errors."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from unittest.mock import patch, MagicMock

def test_app_import():
    """Test that the app.py configuration works."""
    print("Testing app.py configuration...")
    
    # Mock the tools that app.py imports
    with patch('bespoken.tools.FileTool') as mock_file_tool, \
         patch('bespoken.tools.TodoTools') as mock_todo_tools, \
         patch('bespoken.prompts.marimo_prompt') as mock_prompt, \
         patch('llm.get_model') as mock_get_model:
        
        # Set up mocks
        mock_file_tool.return_value = MagicMock()
        mock_todo_tools.return_value = MagicMock()
        mock_prompt = "Mock marimo prompt"
        
        mock_model = MagicMock()
        mock_conversation = MagicMock()
        mock_conversation.responses = []
        mock_conversation.chain.return_value = iter([])
        mock_model.conversation.return_value = mock_conversation
        mock_get_model.return_value = mock_model
        
        # Now try to create the Chat instance like app.py does
        from bespoken import Chat
        
        # Define tools for different modes like in app.py
        file_tool = mock_file_tool("edit.py")
        todo_tools = mock_todo_tools()
        
        chat = Chat(
            model_name="anthropic/claude-3-5-sonnet-20240620",
            tools={
                "development": [file_tool, todo_tools],
                "review": [file_tool], 
                "planning": [],
            },
            mode_switch_messages={
                "development": "You are now in development mode. You can edit files and manage todos. Focus on implementing features and fixing bugs.",
                "review": "You are now in review mode. You can read files to understand the codebase but cannot make changes. Focus on analyzing code and providing feedback.",
                "planning": "You are now in planning mode. You cannot access files or tools. Focus on high-level discussion, architecture planning, and strategic thinking.",
            },
            system_prompt=mock_prompt,
            debug=True,
            initial_mode="development",
            slash_commands={
                "/thinking": "Let me think through this step by step:",
            },
            show_banner=False  # Avoid banner for testing
        )
        
        print(f"✓ Chat instance created successfully")
        print(f"✓ Initial mode: {chat.current_mode}")
        print(f"✓ Available modes: {chat.get_available_modes()}")
        print(f"✓ Mode switching enabled: {chat._is_modes_enabled()}")
        print(f"✓ Can switch to next mode: {chat.switch_to_next_mode()}")
        
        print("✓ App.py configuration works correctly!")

if __name__ == "__main__":
    test_app_import()
    print("\n✅ All app.py import tests passed!")