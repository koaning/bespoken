# Custom Prompts

Bespoken provides a library of prompt templates while allowing you to create your own custom prompts.

## Using Built-in Prompts

Bespoken comes with several pre-built prompt templates:

```python
from bespoken import Bespoken
from bespoken.prompts import general_assistant, code_assistant

app = Bespoken(prompt=general_assistant)

# Or switch to a specialized prompt
app.set_prompt(code_assistant)
```

## Creating Custom Prompts

You can create your own prompts to tailor the behavior of the LLM:

```python
from bespoken.prompts import Prompt

my_prompt = Prompt(
    system="You are a specialized assistant that helps with data analysis.",
    examples=[
        ("Can you analyze this dataset?", "I'd be happy to help analyze your data. Please provide the dataset and specify what kind of analysis you're looking for.")
    ]
)

app.set_prompt(my_prompt)
```

## Dynamic Prompt Generation

Prompts can be dynamically generated based on context:

```python
def create_dynamic_prompt(context):
    return Prompt(
        system=f"You are assisting with {context.task_type}.",
        examples=context.examples
    )

app.set_prompt_generator(create_dynamic_prompt)
```

## Chaining Prompts

You can chain multiple prompts for complex workflows:

```python
from bespoken.prompts import chain_prompts

combined_prompt = chain_prompts([
    analysis_prompt,
    visualization_prompt
])

app.set_prompt(combined_prompt)
```
