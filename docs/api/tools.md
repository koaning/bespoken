# Tools API Reference

This page documents all the tools available in `bespoken.tools`.

## FileSystem

A comprehensive file system operations toolbox that can work with multiple files and directories.

```python
from bespoken.tools import FileSystem

# Initialize the file system tool
fs = FileSystem(working_directory=".")

# Available methods:
# - list_files(directory) - List files and directories
# - read_file(file_path) - Read content from a file
# - write_file(file_path, content) - Write content to a file
# - replace_in_file(file_path, old_string, new_string) - Replace text with diff preview
```

**Key Features:**
- Works with absolute or relative paths
- Shows diffs before applying changes
- Requires user confirmation for replacements
- Handles file encoding properly
- Truncates large files (>50KB) when reading

## FileTool

A single-file editing tool that constrains operations to one specific file.

```python
from bespoken.tools import FileTool

# Create a tool for editing a specific file
tool = FileTool("path/to/file.py")

# Or let the user choose interactively
tool = FileTool()  # Prompts for file path

# Available methods:
# - get_file_path() - Returns the file this tool can access
# - read_file() - Read the file's content
# - replace_in_file(old_string, new_string) - Replace text with diff preview
```

**Key Features:**
- Locked to a single file for safety
- Shows colored diffs with line numbers
- Requires user confirmation for changes
- Cannot access other files

## TodoTools

A simple todo list manager for tracking tasks during your session.

```python
from bespoken.tools import TodoTools

# Initialize the todo tool
todos = TodoTools()

# Available methods:
# - add_todo(task) - Add a new todo item
# - list_todos() - List all todos with status
# - mark_todo_done(index) - Mark a todo as completed (1-based index)
# - flush_todos() - Clear all todos
```

**Example Usage:**
```python
todos.add_todo("Implement new feature")
todos.add_todo("Write tests")
todos.list_todos()  # Shows: 1. [○] Implement new feature, 2. [○] Write tests
todos.mark_todo_done(1)
todos.list_todos()  # Shows: 1. [✓] Implement new feature, 2. [○] Write tests
```

## WebFetchTool

Fetches web content and converts it to markdown for easy processing.

```python
from bespoken.tools import WebFetchTool

# Initialize with optional timeout
web = WebFetchTool(timeout=30)

# Fetch and convert a webpage to markdown
content = web.fetch_url("https://example.com")
```

**Key Features:**
- Converts HTML to clean markdown
- Removes scripts and styles
- Handles errors gracefully
- Configurable timeout

## PlaywrightTool

Browser automation tool for dynamic web interaction (requires `bespoken[browser]` extra).

```python
from bespoken.tools import PlaywrightTool

# Initialize browser tool
browser = PlaywrightTool(headless=False, browser_type="chromium")

# Available methods:
# - navigate(url) - Go to a URL
# - click_text(text) - Click element containing text
# - fill_field(label_or_placeholder, text) - Fill input field
# - screenshot(path) - Take a screenshot
# - get_page_content() - Get current page HTML
# - extract_text() - Extract visible text
# - wait_for_text(text, timeout) - Wait for text to appear
# - close() - Close the browser
```

**Installation:**
```bash
pip install bespoken[browser]
# or
uv pip install "bespoken[browser]"
```

## Command Execution Tools

### run_command

A standalone function for executing shell commands with confirmation.

```python
from bespoken.tools.command import run_command

# Execute any shell command
output = run_command("ls -la", working_directory="/tmp", timeout=30)
```

**Features:**
- Requires user confirmation before execution
- Configurable timeout
- Captures stdout/stderr and exit codes
- Shows command details before execution

### GitTool

Safe git operations with built-in confirmations.

```python
from bespoken.tools.command import GitTool

# Initialize git tool
git = GitTool(auto_trust=False)

# Available methods:
# - status(working_directory) - Get git status
# - log(args, working_directory) - Get git log
# - diff(args, working_directory) - Get git diff
# - branch(args, working_directory) - List branches
```

**Example:**
```python
git.status()  # Shows current git status
git.log("--oneline -5")  # Last 5 commits
git.diff("--staged")  # Show staged changes
```

### NpmTool

Safe npm operations for Node.js projects.

```python
from bespoken.tools.command import NpmTool

# Initialize npm tool
npm = NpmTool(auto_trust=False)

# Available methods:
# - list(depth, working_directory) - List packages
# - outdated(working_directory) - Check outdated packages
# - audit(fix, working_directory) - Security audit
# - scripts(working_directory) - List npm scripts
```

### PythonTool

Python and pip operations with optional UV support.

```python
from bespoken.tools.command import PythonTool

# Initialize with UV support (default)
python = PythonTool(auto_trust=False, uv=True)

# Available methods:
# - version() - Get Python version
# - pip_list(format, working_directory) - List packages
# - pip_show(package, working_directory) - Show package details
# - check_import(module, working_directory) - Test imports
```

## Trust System

Command tools support an auto-trust feature to skip confirmations:

```python
# Trust the tool to skip confirmations
git = GitTool(auto_trust=True)

# Or trust it later via UI
from bespoken import ui
ui.trust_tool("GitTool")
```

## Debug Output

All tools provide debug output when enabled:

```python
from bespoken import chat

chat(
    tools=[FileSystem()],
    debug=True  # Enable debug output
)
```

This shows:
- What the LLM is calling
- Tool status messages
- What the tool returns to the LLM