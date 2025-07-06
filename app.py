from bespoken import chat
from bespoken.tools import FileTool, TodoTools
from bespoken.prompts import marimo_prompt
from bespoken import ui


def save_conversation():
    """Save the current conversation to a file"""
    filename = ui.input("Enter filename: ", completions=["conversation.txt", "chat.md", "session.log"])
    if not filename:
        return "[yellow]Save cancelled[/yellow]"
    
    if ui.confirm(f"Save conversation to {filename}?"):
        # In a real implementation, you'd save the actual conversation
        return f"[green]Conversation saved to {filename}[/green]"
    else:
        return "[yellow]Save cancelled[/yellow]"


def set_role():
    """Set a role for the assistant"""
    roles = ["developer", "teacher", "analyst", "creative writer", "code reviewer"]
    role = ui.choice("What role should I take?", roles)
    return f"You are now acting as a {role}. Please respond in character for this role."


chat(
    model_name="anthropic/claude-3-5-sonnet-20240620",
    tools=[FileTool("edit.py"), TodoTools()],
    system_prompt=marimo_prompt,
    debug=True,
    slash_commands={
        "/thinking": "Let me think through this step by step:",
        "/save": save_conversation,
        "/role": set_role,
        "/formal": "Please respond in a formal, professional manner.",
        "/casual": "Please respond in a casual, friendly way.",
    }
)
