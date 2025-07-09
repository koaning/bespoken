# Quick Start

## Basic Setup

```bash
# Create a new environment
uv venv .venv

# Activate the environment
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows

# Install bespoken
uv install bespoken
```

## Simple Example

Create a file called `simple_chat.py`:

```python
from bespoken import chat
from bespoken.tools import FileTool
from pathlib import Path  # Using pathlib instead of os.path

# Simple chat with file access tool
chat(
    model_name="anthropic/claude-3-5-sonnet-20240620",
    tools=[FileTool(".")],
    system_prompt="You are a helpful assistant."
)
```

Run your script:

```bash
python simple_chat.py
```
