# UI Components API Reference

This page documents the core modules in `src/bespoken/ui`.

## PaddedText

```python
from bespoken.ui import PaddedText

# Display text with consistent padding
PaddedText("Hello, world!")
```

## PaddedInput

```python
from bespoken.ui import PaddedInput

# Get user input with consistent padding
user_input = PaddedInput("Enter your name: ")
```

## SelectInput

```python
from bespoken.ui import SelectInput

# Present multiple choice options
option = SelectInput("Choose an option:", options=["Option 1", "Option 2", "Option 3"])
```

## FileInput

```python
from bespoken.ui import FileInput

# Allow file selection
file_path = FileInput("Select a file:")
```

## Form

```python
from bespoken.ui import Form, TextInput, NumberInput, BooleanInput

# Create a form
form = Form("User Details")
form.add(TextInput("name", "Your name:"))
form.add(NumberInput("age", "Your age:"))
form.add(BooleanInput("subscribe", "Subscribe to newsletter:"))

# Collect user input
user_data = form.collect()
```

## StyledElements

```python
from bespoken.ui import StyledButton, StyledLink, StyledContainer

# Create styled elements
button = StyledButton("Click me", "bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded")
link = StyledLink("Visit docs", "https://example.com/docs", "text-blue-500 hover:text-blue-800")
container = StyledContainer("p-4 border rounded shadow-md")
```
