# Custom Slash Commands

Bespoken provides a powerful slash command system that allows users to trigger specific actions during conversations.

## How Slash Commands Work

Slash commands are triggered by typing `/` followed by a command name:

```
/help
/run python -c "print('Hello world')"
/search query
```

These commands are intercepted by Bespoken and processed according to their defined behavior.

## Built-in Commands

Bespoken comes with several built-in slash commands:

- `/help`: Displays available commands
- `/clear`: Clears the current conversation
- `/run`: Executes a command

## Creating Custom Commands

You can create your own slash commands:

```python
from bespoken import Bespoken, SlashCommand

def my_command(args):
    return f"Command executed with args: {args}"

app = Bespoken()
app.register_command(SlashCommand("custom", my_command, "My custom command"))
```

## Command Arguments

Slash commands can accept arguments that are passed to the handler function:

```python
def echo(args):
    return f"Echo: {' '.join(args)}"

app.register_command(SlashCommand("echo", echo, "Echo back the provided arguments"))
```
