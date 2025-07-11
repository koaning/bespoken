# Prompts API Reference

This page documents the prompts available in `bespoken.prompts`.

## Available Prompts

### marimo_prompt

A specialized prompt for creating data science notebooks using marimo.

```python
from bespoken.prompts import marimo_prompt
from bespoken import chat

# Use the marimo prompt for notebook assistance
chat(
    model_name="anthropic/claude-3-5-sonnet-20240620",
    system_prompt=marimo_prompt,
    tools=[FileTool("notebook.py")]
)
```

**Key Features:**
- Specialized for marimo notebook development
- Prefers polars over pandas for data manipulation
- Prefers altair over matplotlib for visualization
- Understands marimo's cell-based structure with `@app.cell` decorators
- Knows about marimo's reactive programming model
- Includes UV script dependencies format

**Example marimo file structure the prompt understands:**
```python
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "numpy==2.3.1",
# ]
# ///

import marimo

__generated_with = "0.14.10"
app = marimo.App(width="columns")

@app.cell
def _():
    import marimo as mo
    import numpy as np
    return mo, np

@app.cell
def _(mo):
    slider = mo.ui.slider(1, 10, 1)
    slider
    return (slider,)

if __name__ == "__main__":
    app.run()
```

## Using Custom Prompts

You can create your own system prompts to customize the assistant's behavior:

```python
from bespoken import chat

# Define a custom prompt
my_prompt = """You are an expert Python developer specializing in web applications.
You prefer FastAPI for APIs and focus on clean, maintainable code.
Always include type hints and proper error handling."""

# Use the custom prompt
chat(
    model_name="anthropic/claude-3-5-sonnet-20240620",
    system_prompt=my_prompt,
    tools=[FileSystem()]
)
```

## Prompt Best Practices

### 1. Be Specific About Preferences
```python
prompt = """You are a data analysis assistant.
Preferences:
- Use polars for data manipulation (not pandas)
- Use plotly for interactive visualizations
- Always validate data types before operations
- Include docstrings for all functions"""
```

### 2. Include Context About the Project
```python
prompt = """You are helping with a Django web application.
Project structure:
- apps/ contains Django apps
- Use Django 4.2 features
- Follow the project's existing patterns
- Tests go in tests/ directory"""
```

### 3. Set Behavioral Guidelines
```python
prompt = """You are a helpful coding assistant.
Guidelines:
- Ask for clarification when requirements are unclear
- Suggest test cases for new functions
- Point out potential security issues
- Explain complex logic with comments"""
```

## Combining Prompts with Tools

Different prompts work best with different tools:

```python
# For file editing tasks
from bespoken.prompts import marimo_prompt
from bespoken.tools import FileTool

chat(
    system_prompt=marimo_prompt,
    tools=[FileTool("analysis.py")]
)

# For system administration
admin_prompt = "You are a system administrator assistant..."
from bespoken.tools.command import GitTool, run_command

chat(
    system_prompt=admin_prompt,
    tools=[GitTool(), run_command]
)
```

## Dynamic Prompt Modification

You can modify prompts during runtime using slash commands:

```python
from bespoken import chat, ui

def change_style():
    """Change the coding style preference"""
    styles = ["functional", "object-oriented", "procedural"]
    style = ui.choice("Select coding style:", styles)
    return f"From now on, prefer {style} programming style."

chat(
    system_prompt="You are a Python developer.",
    slash_commands={
        "/style": change_style
    }
)
```

## Future Prompts

The prompts module is designed to be extensible. Future additions may include:

- `web_developer_prompt` - For web development tasks
- `devops_prompt` - For DevOps and infrastructure
- `api_designer_prompt` - For API design and documentation
- `test_writer_prompt` - For writing comprehensive tests

To request new prompts or contribute your own, please visit the [GitHub repository](https://github.com/koaning/bespoken).