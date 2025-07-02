# bespoken

Tools to build your own "taskmaster" - an AI-powered coding assistant with interactive file editing and web automation capabilities.

## Installation

Basic installation:
```bash
pip install bespoken
```

With browser automation support (Playwright):
```bash
pip install 'bespoken[browser]'
playwright install  # Download browser binaries
```

## Features

- **FileSystem**: Work with multiple files and directories
- **FileTool**: Edit a single file with interactive confirmations
- **TodoTools**: Manage tasks during your coding session
- **WebFetchTool**: Fetch and convert web content to markdown
- **PlaywrightTool**: Browser automation for dynamic web interactions (optional)

## Usage

```python
from bespoken import chat
from bespoken.tools import FileTool, TodoTools

chat(
    model_name="anthropic/claude-3-5-sonnet-20240620",
    tools=[FileTool("edit.py"), TodoTools()],
    system_prompt="You are a coding assistant.",
    debug=False,
)
```
