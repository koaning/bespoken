from bespoken import chat
from bespoken.tools import FileTool, TodoTools, PlaywrightTool
from bespoken.prompts import marimo_prompt


chat(
    model_name="anthropic/claude-3-5-sonnet-20240620",
    tools=[FileTool("edit.py"), TodoTools()],
    system_prompt=marimo_prompt,
    debug=True,
)
