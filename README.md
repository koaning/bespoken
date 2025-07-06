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

If you now run this Python file, a chat appears on command line. 

## Features 

### Autocomplete 

Tab completion for commands and file paths. Use `@file.py` to get file path suggestions, "/" + <kbd>TAB></kbd> to autocomplete commands or use arrow keys for command history.

![parrot](https://github.com/user-attachments/assets/284ce287-ecc6-4beb-8fb5-6df77d3704f7)

### Custom slash commands

Define your own `/commands` that either send text to the LLM or trigger interactive functions:

```python
def save_conversation():
    """Save conversation to file"""
    filename = ui.input("Filename: ")
    return f"Saved to {filename}"

chat(
    ...,
    slash_commands={
        "/save": save_conversation,
        "/formal": "Please respond in a formal manner.",
    }
)
```

### Custom agents 

The whole point of this library is to make it easy to make custom agents for different use-cases. You could, for example, have a few custom tools with a custom prompt and a bespoke LLM model for your use-case.

## Why? 

The goal is to host a bunch of tools that you can pass to the LLM, but the main idea here is that you can also make it easy to constrain the chat. The `FileTool`, for example, only allows the LLM to make edits to a single file declared upfront. This significantly reduces any injection risks and still covers a lot of use-cases. It is also a nice exercize to make tools like claude code feel less magical, and you can also swap out the LLM with any other one as you see fit. 

This project is in early days at the moment, but it feels exciting to work on!
