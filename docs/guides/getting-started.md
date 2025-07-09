# Getting Started with Bespoken

## Installation

Bespoken can be installed using `uv`, a faster and more reliable Python package installer:

```bash
uv install bespoken
```

## Quick Setup

To create a new environment with Bespoken:

```bash
uv venv .venv
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows
```

## Basic Usage

Here's a simple example of using Bespoken:

```python
from bespoken import Bespoken
from pathlib import Path  # Using pathlib instead of os.path

app = Bespoken()
app.run()
```

## Next Steps

- Explore the [Tools](tools.md) guide to learn how to use and create tools
- Check out the [UI Components](ui-components.md) to enhance your user interface
- Learn about [Custom Prompts](custom-prompts.md) to tailor LLM interactions
