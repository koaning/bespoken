## Quickstart

This is the simplest quickstart for an agent that can only make changes to a Python file.

```python title="app.py"
from bespoken import chat
from bespoken.tools import FileTool
from bespoken import ui

def set_role():
    """Set a voice for the assistant"""
    roles = ["pirate", "teacher", "professor"]
    role = ui.choice("What role should I take?", roles)
    return f"You are now speaking like a {role}. Please respond in character for this role."

chat(
    model_name="anthropic/claude-3-5-sonnet-20240620",
    tools=[FileTool("edit.py")],
    system_prompt="You are a helpful assistant.",
    debug=False,
    slash_commands={
        "/role": set_role,
    }
)
```

