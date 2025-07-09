# Prompts API Reference

This page documents the core modules in `src/bespoken/prompts`.

## Prompt

```python
from bespoken.prompts import Prompt

# Create a basic prompt
prompt = Prompt(
    system="You are a helpful assistant.",
    examples=[
        ("What's the weather?", "I don't have access to current weather data. To get weather information, you would need to specify a location and I would need access to a weather API.")
    ]
)
```

## Built-in Prompts

```python
from bespoken.prompts import general_assistant, code_assistant, data_assistant

# Use a general-purpose assistant prompt
app.set_prompt(general_assistant)

# Switch to a specialized prompt for coding tasks
app.set_prompt(code_assistant)

# Use a data analysis focused prompt
app.set_prompt(data_assistant)
```

## Prompt Chaining

```python
from bespoken.prompts import chain_prompts

# Chain multiple prompts together
combined_prompt = chain_prompts([
    first_prompt,
    second_prompt,
    third_prompt
])
```

## Dynamic Prompts

```python
from bespoken.prompts import PromptTemplate

# Create a template with placeholders
template = PromptTemplate(
    "You are assisting with {task_type}. The user's name is {user_name}."
)

# Fill in the template
prompt = template.format(task_type="data analysis", user_name="Alice")
```
