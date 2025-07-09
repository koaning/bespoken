# Tools in Bespoken

## Tool Constraints

Bespoken allows you to constrain the LLM to only use specific tools, providing controlled access to functionality:

```python
from bespoken import Bespoken, GitTool, PythonTool

app = Bespoken(tools=[GitTool(), PythonTool()])
```

This approach ensures that the LLM can only perform actions through the explicitly provided tools.

## Available Tools

Bespoken comes with several built-in tools:

- **GitTool**: Provides git functionality
- **NpmTool**: Manages Node.js packages
- **PythonTool**: Executes Python code

## Trust System

The trust system in Bespoken ensures that sensitive operations require explicit permission:

```python
tool = GitTool(trusted=False)  # Will require confirmation for each operation
```

## Creating Custom Tools

You can create your own tools by extending the base Tool class:

```python
from bespoken.tools import Tool

class MyCustomTool(Tool):
    def __init__(self):
        super().__init__(name="custom", description="My custom tool")
    
    def run(self, args):
        # Tool implementation
        return {"result": "Success"}
```
