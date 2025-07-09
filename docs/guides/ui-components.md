# UI Components

Bespoken provides a set of UI components that make it easy for users to interact with your application.

## Padding System

Bespoken uses a consistent UI padding system to ensure visual harmony across components:

```python
from bespoken.ui import PaddedText, PaddedInput

# Display text with consistent padding
PaddedText("Hello, world!")

# Get user input with matching padding
user_input = PaddedInput("Enter your name: ")
```

## Interactive Components

Interactive components allow users to provide input during conversations:

```python
from bespoken.ui import SelectInput, FileInput

# Present multiple choice options
option = SelectInput("Choose an option:", ["Option 1", "Option 2", "Option 3"])

# Allow file selection
file_path = FileInput("Select a file:")
```

## Form Integration

You can create dynamic forms that appear when additional input is needed:

```python
from bespoken.ui import Form, TextInput, NumberInput

form = Form("User Details")
form.add(TextInput("name", "Your name:"))
form.add(NumberInput("age", "Your age:"))

user_data = form.collect()
```

## Styling with Tailwind CSS

Bespoken uses Tailwind CSS (via CDN) for styling components:

```python
from bespoken.ui import StyledButton

# Create a button with Tailwind classes
button = StyledButton("Click me", "bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded")
```
