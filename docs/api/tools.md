# Tools API Reference

This page documents the core modules in `src/bespoken/tools`.

## Base Tool

```python
from bespoken.tools import Tool

class Tool:
    """Base class for all tools."""
    
    def __init__(self, name, description, trusted=False):
        """
        Initialize a tool.
        
        Args:
            name (str): Name of the tool
            description (str): Description of what the tool does
            trusted (bool): Whether the tool is trusted to run without confirmation
        """
        pass
        
    def run(self, args):
        """
        Run the tool with the given arguments.
        
        Args:
            args (list): Arguments for the tool
            
        Returns:
            dict: Result of the tool execution
        """
        pass
```

## GitTool

```python
from bespoken.tools import GitTool

# Initialize a git tool
git_tool = GitTool(trusted=False)

# Use the git tool
result = git_tool.run(["status"])
```

## PythonTool

```python
from bespoken.tools import PythonTool

# Initialize a Python tool
python_tool = PythonTool(trusted=False)

# Execute Python code
result = python_tool.run(["-c", "print('Hello, world!')"])
```

## NpmTool

```python
from bespoken.tools import NpmTool

# Initialize an NPM tool
npm_tool = NpmTool(trusted=False)

# Install a package
result = npm_tool.run(["install", "lodash"])
```
