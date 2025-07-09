# Configuration

## Basic Configuration

Bespoken can be configured when initializing the chat:

```python
from bespoken import chat
from pathlib import Path

chat(
    model_name="anthropic/claude-3-5-sonnet-20240620",
    system_prompt="You are a helpful assistant.",
    debug=True,  # Enable debug mode
    history_file=Path("chat_history.json"),  # Save chat history
)
```

## Available Settings

| Parameter | Type | Description |
|-----------|------|-------------|
| `model_name` | str | Name of the LLM to use |
| `system_prompt` | str | System prompt for the LLM |
| `tools` | list | List of tools to provide to the LLM |
| `debug` | bool | Enable debug mode |
| `history_file` | Path | File to save chat history |
| `slash_commands` | dict | Custom slash commands |
