import srsly
from pathlib import Path
import json

from bespoken import Chat
from bespoken.tools import FileTool, TodoTools
from bespoken.prompts import marimo_prompt
from bespoken import ui
from bespoken import config

def set_role():
    """Set a role for the assistant"""
    roles = ["developer", "teacher", "analyst", "creative writer", "code reviewer"]
    role = ui.choice("What role should I take?", roles)
    return f"You are now acting as a {role}. Please respond in character for this role."


def debug_reason():
    """Set a role for the assistant"""
    ui.tool_status("We are going to prompt the LLM to see if they can find the bug in the code on their own.")
    entrypoint = ui.input("What is the entrypoint for the user?")
    action = ui.input("What is the action the user is trying to take?")
    out = f"""You've introduced a new bug, but instead of me telling you what the bug is, let's see if you can find it for yourself. Imagine that you are a user and that you start by {entrypoint}. Go through all the steps that would happen if a user tries to {action}. Think through all the steps and see if you can spot something that could go wrong. Don't write any code, but let's see if we both find the same issue."""
    print("")
    ui.print_neutral(out)
    return out


# Define tools for different modes
file_tool = FileTool("edit.py")
todo_tools = TodoTools()

Chat(
    model_name="anthropic/claude-3-5-sonnet-20240620",
    tools={
        "development": [file_tool, todo_tools],  # Full development capabilities
        "review": [file_tool],  # Code review mode - can read files but no todo management
        "planning": [],  # Planning mode - no tools, pure discussion
    },
    mode_switch_messages={
        "development": "You are now in development mode. You can edit files and manage todos. Focus on implementing features and fixing bugs.",
        "review": "You are now in review mode. You can read files to understand the codebase but cannot make changes. Focus on analyzing code and providing feedback.",
        "planning": "You are now in planning mode. You cannot access files or tools. Focus on high-level discussion, architecture planning, and strategic thinking.",
    },
    system_prompt=marimo_prompt,
    debug=True,
    initial_mode="development",
    slash_commands={
        "/thinking": "Let me think through this step by step:",
        "/role": set_role,
        "/debug_prompt": debug_reason,
    },
    history_callback=lambda x: srsly.write_jsonl(Path("logs.json"), x, append=True, append_new_line=False)
).run()
