---
hide:
  - navigation
  - toc
---

# Bespoken

## What is Bespoken?

Bespoken is a framework that allows you to create custom LLM agents for the command line. It provides a simple yet powerful interface for building applications that leverage large language models in a controlled and user-friendly way.

![intro](static/intro.svg)

## How Bespoken Works

The easiest way to explain how `bespoken` works is to show you an example. 

```python title="app.py"
from bespoken import chat
from bespoken.tools import FileTool, TodoTools
from bespoken.prompts import marimo_prompt
from bespoken import ui

def set_role():
    """Set a voice for the assistant"""
    roles = ["pirate", "teacher", "professor"]
    role = ui.choice("What role should I take?", roles)
    return f"You are now speaking like a {role}. Please respond in character for this role."

chat(
    model_name="anthropic/claude-3-5-sonnet-20240620",
    tools=[FileTool("edit.py"), TodoTools()],
    system_prompt=marimo_prompt,
    debug=False,
    slash_commands={
        "/role": set_role,
    }
)
```

You can run this app via `uv run app.py` and you will get an agent experience that is constrained and bespoke to your needs.

### How does it work?

Bespoken builds on top of the [llm](https://llm.datasette.io/en/stable/) tool created by [Simon Willison](https://simonwillison.net/). This gives us ample LLMs to pick from, some of which support "tools".

> Tools are a way to give an LLM the ability to perform actions on your behalf. You can define these as normal Python functions/classes and, assuming that you've given them good names and docstrings, the LLM can use them when it deems it appropriate. This library provides you with plenty of tools out of the box, but you can also define your own. The whole point is that you only give the LLM access to the tools it needs to perform its task.

Besides tools this library also allows you to customise the system prompt and you can also define "slash commands". 

> Slash commands are a way to give an LLM the ability to perform actions on your behalf. Unlike a tool, the LLM does not trigger it, you do! Some of these commands are pre-defined prompts that you like to use while debugging while others might allow you to make a commit manually from within the chat interface (that way you won't waste precious tokens). We ship with some pre-defined commands but the whole point is that you can also configure your own. 

One of the main features of bespoken is that we also give you lego bricks in `bespoken.ui` to make the ui feel nice. 

## Custom Slash Commands

Bespoken introduces a slash command system that enhances user interaction:

- Create custom commands that trigger specific behaviors
- Use `/` followed by a command name to execute predefined actions
- Extend functionality through user-defined slash commands
- Provide shortcuts to common operations

## UI Components for Interactive Input

The UI components in Bespoken make it easy for users to provide input during conversations:

- Dynamic form elements that appear when additional input is needed
- Consistent padding system for visual harmony
- Interactive components that guide users through complex operations
- Seamless integration of user input into the LLM workflow

## Prompts Library and Customization

Bespoken comes with a set of useful prompts but is designed for customization:

- Pre-built prompt templates for common use cases
- Simple API for creating and modifying prompts
- Ability to chain prompts for complex workflows
- Support for dynamic prompt generation based on context

## API Documentation

### Core Modules

- **`src/bespoken/tools`**: Tools that extend LLM capabilities
- **`src/bespoken/ui`**: User interface components
- **`src/bespoken/prompts`**: Prompt templates and utilities
