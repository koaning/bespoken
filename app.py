from bespoken import chat
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


chat(
    model_name="anthropic/claude-3-5-sonnet-20240620",
    tools=[FileTool("edit.py"), TodoTools()],
    system_prompt=marimo_prompt,
    debug=True,
    slash_commands={
        "/thinking": "Let me think through this step by step:",
        "/role": set_role,
        "/debug_prompt": debug_reason,
    }
)
