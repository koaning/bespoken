from bespoken import chat
from bespoken.tools import FileTool

chat(
    model_name="anthropic/claude-3-5-sonnet-20240620",
    tools=[FileTool("edit.py")],
    system_prompt="You are a coding assistant that can make edits to a single file that is defined by the filetool.",
    debug=False,
)
