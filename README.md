# bespoken

```

██████╗ ███████╗███████╗██████╗  ██████╗ ██╗  ██╗███████╗███╗   ██╗
██╔══██╗██╔════╝██╔════╝██╔══██╗██╔═══██╗██║ ██╔╝██╔════╝████╗  ██║
██████╔╝█████╗  ███████╗██████╔╝██║   ██║█████╔╝ █████╗  ██╔██╗ ██║
██╔══██╗██╔══╝  ╚════██║██╔═══╝ ██║   ██║██╔═██╗ ██╔══╝  ██║╚██╗██║
██████╔╝███████╗███████║██║     ╚██████╔╝██║  ██╗███████╗██║ ╚████║
╚═════╝ ╚══════╝╚══════╝╚═╝      ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝


A terminal chat experience that you can configure yourself.
```

## Installation

Basic installation:

```bash
uv pip install bespoken
```

## Usage

This library uses [llm](https://llm.datasette.io/en/stable/) under the hood to provide you with building blocks to make chat interfaces from the commandline. Here's an example. 

```python
from bespoken import chat
from bespoken.tools import FileTool, TodoTools, PlaywrightTool

chat(
    model_name="anthropic/claude-3-5-sonnet-20240620",
    tools=[FileTool("edit.py"), TodoTools(), PlaywrightTool()],
    system_prompt="You are a coding assistant that can make edits to a single file that is defined by the filetool.",
    debug=True,
)
```

The goal is to host a bunch of tools that you can pass to the LLM, but the main idea here is that you can also make it easy to constrain the chat. The `FileTool`, for example, only allows the LLM to make edits to a single file declared upfront. This significantly reduces any injection risks and still covers a lot of use-cases. 

This project is in early days at the moment, but it feels exciting to work on!
