# Quickstart
## Single file agent

This is the simplest quickstart for an agent that can only make changes to a Python file. We will use claude for this, which means we first need to install it. 

```bash
uv pip install llm-anthropic
```

You also need to make sure that you have an API key for claude. You can get one from [Anthropic](https://console.anthropic.com/api-keys) and you can configure it in a `.env` file by configuring the `ANTHROPIC_API_KEY` environment variable.

With that out of the way, here's the app definition.

```python title="app.py"
from bespoken import chat
from bespoken.tools import FileTool
from bespoken import ui

def set_role():
    """Set a voice for the assistant"""
    roles = ["pirate", "teacher", "professor"]
    role = ui.choice("What role should I take?", roles)
    return f"You are now speaking like a {role}. Please respond in character for this role."

chat(
    model_name="anthropic/claude-3-5-sonnet-20240620",
    tools=[FileTool("edit.py")],
    system_prompt="You are a helpful assistant.",
    debug=False,
    slash_commands={
        "/role": set_role,
    }
)
```

You can run this app via `uv run app.py` and you will get an agent. 

## Local model agent

The [llm package](https://llm.datasette.io/en/stable/other-models.html) also supports local models via [ollama](https://ollama.com/), so let's try that out. First you need to make the [llm-ollama](https://github.com/taketwo/llm-ollama) package is installed. 

```
uv run llm install llm-ollama
```

Next, you should be able to run `ollama list` to see all the models available to ollama. These models should now also appear when you run:

```
uv run llm models | grep Ollama
```

Be aware that you can't use every ollama model. When you try to run `gemma3:1b` you'll get a `ValueError` because it doesn't support tools. You can find supported Ollama models on their [docs](https://ollama.com/search?c=tools). At the time of making these docs the `qwen3:0.6b` model was the lightest model that supported tools so we'll use that in our demo below.

```python title="app.py"
from bespoken import chat
from bespoken.tools import FileTool
from bespoken import ui

def set_role():
    """Set a voice for the assistant"""
    roles = ["pirate", "teacher", "professor"]
    role = ui.choice("What role should I take?", roles)
    return f"You are now speaking like a {role}. Please respond in character for this role."

chat(
    model_name="qwen3:0.6b",
    tools=[FileTool("blogpost.md")],
    system_prompt="You are a helpful writing assistant.",
    debug=False,
    slash_commands={
        "/role": set_role,
    }
)
```
