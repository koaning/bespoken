# Slash Commands API Reference

This page documents how to create and use slash commands in bespoken.

## What are Slash Commands?

Slash commands are user-triggered actions that start with `/`. Unlike tools (which the LLM calls), slash commands are executed directly by the user during a chat session.

## Basic Usage

```python
from bespoken import chat, ui

def hello_command():
    """Say hello to the user"""
    return "Hello! How can I help you today?"

def clear_screen():
    """Clear the terminal screen"""
    import os
    os.system('clear' if os.name == 'posix' else 'cls')
    return "Screen cleared!"

chat(
    model_name="anthropic/claude-3-5-sonnet-20240620",
    slash_commands={
        "/hello": hello_command,
        "/clear": clear_screen,
    }
)
```

## Commands with User Input

Slash commands can interact with the user through UI components:

```python
from bespoken import chat, ui

def set_role():
    """Set a voice for the assistant"""
    roles = ["pirate", "teacher", "professor", "casual", "formal"]
    role = ui.choice("What role should I take?", roles)
    return f"You are now speaking like a {role}. Please respond in character for this role."

def set_temperature():
    """Adjust response creativity"""
    temp = ui.input("Enter temperature (0.0-1.0): ")
    try:
        temp_float = float(temp)
        if 0 <= temp_float <= 1:
            return f"Temperature set to {temp_float}. My responses will be {'more creative' if temp_float > 0.7 else 'more focused'}."
        else:
            return "Temperature must be between 0.0 and 1.0"
    except ValueError:
        return "Invalid temperature value"

chat(
    slash_commands={
        "/role": set_role,
        "/temp": set_temperature,
    }
)
```

## File Operations Commands

```python
from bespoken import chat, ui
from pathlib import Path

def save_conversation():
    """Save the conversation to a file"""
    filename = ui.input("Enter filename (without extension): ")
    # In a real implementation, you'd access conversation history
    Path(f"{filename}.txt").write_text("Conversation saved!")
    return f"Conversation saved to {filename}.txt"

def load_context():
    """Load a file as context"""
    filepath = ui.input("Enter file path: ")
    try:
        content = Path(filepath).read_text()
        return f"Loaded {len(content)} characters from {filepath}. I'll keep this in mind."
    except Exception as e:
        return f"Error loading file: {e}"

chat(
    slash_commands={
        "/save": save_conversation,
        "/load": load_context,
    }
)
```

## Git Integration Commands

```python
from bespoken import chat, ui
import subprocess

def git_status():
    """Show git status"""
    result = subprocess.run(["git", "status"], capture_output=True, text=True)
    return f"Git status:\n{result.stdout}"

def git_commit():
    """Make a git commit"""
    message = ui.input("Enter commit message: ")
    
    # Stage all changes
    subprocess.run(["git", "add", "."])
    
    # Commit
    result = subprocess.run(
        ["git", "commit", "-m", message], 
        capture_output=True, 
        text=True
    )
    
    if result.returncode == 0:
        return f"Successfully committed: {message}"
    else:
        return f"Commit failed: {result.stderr}"

chat(
    slash_commands={
        "/status": git_status,
        "/commit": git_commit,
    }
)
```

## Advanced Command Patterns

### Commands with Multiple Steps

```python
def configure_project():
    """Interactive project configuration"""
    # Step 1: Project type
    project_type = ui.choice(
        "What type of project?", 
        ["Web App", "CLI Tool", "Library", "Data Science"]
    )
    
    # Step 2: Language
    language = ui.choice(
        "Primary language?",
        ["Python", "JavaScript", "TypeScript", "Go"]
    )
    
    # Step 3: Confirmation
    if ui.confirm(f"Configure as {language} {project_type}?"):
        return f"""Project configured!
Type: {project_type}
Language: {language}

I'll now assist you with {language} best practices for {project_type} development."""
    else:
        return "Configuration cancelled."
```

### Commands that Modify Behavior

```python
def toggle_verbose():
    """Toggle verbose mode"""
    # This would typically modify a global state
    import bespoken.config
    bespoken.config.DEBUG_MODE = not bespoken.config.DEBUG_MODE
    status = "on" if bespoken.config.DEBUG_MODE else "off"
    return f"Verbose mode is now {status}"

def set_model():
    """Change the LLM model"""
    models = [
        "anthropic/claude-3-5-sonnet-20240620",
        "openai/gpt-4",
        "anthropic/claude-3-opus-20240229"
    ]
    model = ui.choice("Select model:", models)
    # In practice, this would update the chat configuration
    return f"Model changed to {model} (will take effect in next session)"
```

### Commands with Error Handling

```python
def run_tests():
    """Run project tests"""
    test_framework = ui.choice(
        "Test framework?",
        ["pytest", "unittest", "jest", "go test"]
    )
    
    try:
        if test_framework == "pytest":
            result = subprocess.run(
                ["pytest", "-v"], 
                capture_output=True, 
                text=True,
                timeout=30
            )
        # Handle other frameworks...
        
        if result.returncode == 0:
            return f"All tests passed!\n{result.stdout}"
        else:
            return f"Tests failed:\n{result.stdout}\n{result.stderr}"
            
    except subprocess.TimeoutExpired:
        return "Tests timed out after 30 seconds"
    except FileNotFoundError:
        return f"{test_framework} not found. Please install it first."
    except Exception as e:
        return f"Error running tests: {e}"
```

## Built-in Commands

Bespoken may include some built-in commands:

- `/help` - Show available commands
- `/exit` or `/quit` - Exit the chat session
- `/clear` - Clear the screen
- `/debug` - Toggle debug mode

These can be overridden by providing your own implementations.

## Best Practices

1. **Clear Names**: Use descriptive command names that indicate the action
   ```python
   # Good
   "/save-chat", "/set-model", "/run-tests"
   
   # Less clear
   "/s", "/m", "/t"
   ```

2. **Help Text**: Always include docstrings
   ```python
   def my_command():
       """Brief description of what this command does"""
       # Implementation
   ```

3. **User Feedback**: Always return a message indicating what happened
   ```python
   def good_command():
       # Do something
       return "Successfully completed the action!"
   
   def bad_command():
       # Do something
       # No return - user won't know if it worked
   ```

4. **Error Handling**: Handle errors gracefully
   ```python
   def safe_command():
       try:
           # Risky operation
           result = perform_operation()
           return f"Success: {result}"
       except SpecificError as e:
           return f"Operation failed: {e}"
       except Exception as e:
           return f"Unexpected error: {e}"
   ```

5. **Confirm Destructive Actions**: Use `ui.confirm()` for dangerous operations
   ```python
   def delete_files():
       if ui.confirm("Delete all temporary files?", default=False):
           # Perform deletion
           return "Files deleted"
       return "Deletion cancelled"
   ```

## Example: Complete Chat with Commands

```python
from bespoken import chat, ui
from bespoken.tools import FileTool, TodoTools

def set_role():
    """Change assistant personality"""
    roles = ["helpful", "concise", "detailed", "creative"]
    role = ui.choice("Select communication style:", roles)
    return f"I'll be {role} in my responses."

def show_stats():
    """Show session statistics"""
    # In a real implementation, track these
    return """Session Statistics:
- Messages: 42
- Tools used: 7
- Files edited: 3
- Time elapsed: 15 minutes"""

def take_break():
    """Remind to take a break"""
    minutes = ui.input("Remind me in how many minutes? ")
    return f"I'll remind you to take a break in {minutes} minutes. Keep coding!"

# Create a comprehensive chat interface
chat(
    model_name="anthropic/claude-3-5-sonnet-20240620",
    tools=[FileTool("main.py"), TodoTools()],
    system_prompt="You are a helpful coding assistant.",
    slash_commands={
        "/role": set_role,
        "/stats": show_stats,
        "/break": take_break,
    }
)
```

When the user types `/role`, they'll be prompted to choose a communication style, and the assistant will adjust accordingly.