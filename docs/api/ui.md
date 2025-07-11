# UI Components API Reference

This page documents all the UI components available in `bespoken.ui`.

## Core Display Functions

### print
```python
from bespoken.ui import print

# Print text with consistent left padding
print("Hello, world!")
print("Multi-line\ntext\nis properly padded", indent=4)
```

### print_empty_line
```python
from bespoken.ui import print_empty_line

# Print an empty line with padding (maintains visual consistency)
print_empty_line()
print_empty_line(indent=4)
```

### print_neutral
```python
from bespoken.ui import print_neutral

# Print text in neutral gray color with wrapping
print_neutral("This is some neutral information that will wrap properly.")
```

## Tool Status Messages

These functions are used by tools to provide feedback:

### tool_status
```python
from bespoken.ui import tool_status

# Print a cyan status message with extra whitespace
tool_status("Preparing to execute command...")
```

### tool_debug
```python
from bespoken.ui import tool_debug

# Print debug info in magenta (only when DEBUG_MODE is True)
tool_debug(">>> LLM calling tool: read_file()")
```

### tool_error
```python
from bespoken.ui import tool_error

# Print error message in red
tool_error("Failed to connect to server")
```

### tool_success
```python
from bespoken.ui import tool_success

# Print success message in green
tool_success("Operation completed successfully")
```

### tool_warning
```python
from bespoken.ui import tool_warning

# Print warning message in yellow
tool_warning("This action may take a while...")
```

## User Input Functions

### input
```python
from bespoken.ui import input

# Get basic input with padding
name = input("Enter your name: ")

# With auto-completion
languages = ["python", "javascript", "rust", "go"]
lang = input("Choose language: ", completions=languages)
```

**Features:**
- File path auto-completion with `@` prefix
- Command history with up/down arrows
- Auto-suggestions from history
- Custom completions support

### confirm
```python
from bespoken.ui import confirm

# Ask for yes/no confirmation
if confirm("Continue with operation?"):
    # proceed
    pass

# With custom default
confirm("Delete file?", default=False)
```

### choice
```python
from bespoken.ui import choice

# Present multiple choice selection
option = choice("Select an option:", ["Option A", "Option B", "Option C"])

# Supports keyboard shortcuts (numbers)
role = choice("What role should I take?", ["pirate", "teacher", "professor"])
```

## Streaming Output

For displaying LLM responses with proper word wrapping:

### stream
```python
from bespoken.ui import stream

# Stream chunks of text with word-aware wrapping
chunks = ["Hello ", "world! ", "This is a long sentence that will wrap properly."]
stream(chunks)
```

### start_streaming / stream_chunk / end_streaming
```python
from bespoken.ui import start_streaming, stream_chunk, end_streaming

# For manual streaming control
start_streaming()
stream_chunk("First chunk ")
stream_chunk("with more text")
end_streaming()
```

## Banner and Customization

### show_banner
```python
from bespoken.ui import show_banner

# Display the default bespoken ASCII art banner
show_banner()
```

### set_ascii_art
```python
from bespoken.ui import set_ascii_art

# Customize the banner
custom_art = """
  _____ _    _ ____ _______ ____  __  __ 
 / ____| |  | / ___|__   __/ __ \|  \/  |
| |    | |  | \___ \  | | | |  | | \  / |
| |    | |  | |___) | | | | |  | | |\/| |
| |____| |__| |____/  | | | |__| | |  | |
 \_____|____/ |_____| |_|  \____/|_|  |_|
"""

set_ascii_art(custom_art, subtitle="My Custom Tool v1.0")
show_banner()
```

## Tool Trust System

Manage which tools require confirmation:

### trust_tool / untrust_tool / is_tool_trusted
```python
from bespoken.ui import trust_tool, untrust_tool, is_tool_trusted

# Trust a tool (no confirmation needed)
trust_tool("GitTool")

# Check if trusted
if is_tool_trusted("GitTool"):
    print("Git operations won't ask for confirmation")

# Remove trust
untrust_tool("GitTool")
```

### confirm_tool_action
```python
from bespoken.ui import confirm_tool_action

# Used internally by tools to request confirmation
if confirm_tool_action(
    "GitTool",
    "Execute: git commit -m 'Fix bug'",
    {"Working directory": "/home/user/project"}
):
    # Execute the action
    pass
```

## Global Configuration

### Padding Constants
```python
from bespoken.ui import LEFT_PADDING, RIGHT_PADDING

# Default padding values
# LEFT_PADDING = 2
# RIGHT_PADDING = 2
```

These values control the consistent indentation throughout the UI.

## Console Access

For advanced usage, you can access the Rich console:

```python
from bespoken.ui import _console

# Direct console access (use sparingly)
_console.rule("Section Break")
```

## Example: Building a Custom Tool with UI

```python
from bespoken.ui import tool_status, tool_success, tool_error, confirm
import llm

class CustomTool(llm.Toolbox):
    """Example tool using UI components."""
    
    def process_data(self, data: str) -> str:
        tool_status(f"Processing {len(data)} characters...")
        
        if not confirm("This will modify data. Continue?"):
            tool_error("Operation cancelled by user")
            return "Cancelled"
        
        # Process the data...
        result = data.upper()
        
        tool_success(f"Processed successfully!")
        return result
```

## Best Practices

1. **Consistency**: Always use the UI functions instead of raw print() for consistent padding
2. **Colors**: Use status functions appropriately (error=red, success=green, etc.)
3. **Confirmations**: Use confirm() for destructive or important operations
4. **Streaming**: Use the streaming functions for LLM output to ensure proper word wrapping
5. **Trust**: Only trust tools that are safe to run without confirmation