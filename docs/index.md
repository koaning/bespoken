---
hide:
  - navigation
---

<style>
    .container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem;
    }
    
    .ascii-logo {
        font-size: 0.8rem;
        line-height: 1.2;
        margin-bottom: 1.5rem;
        display: inline-block;
        animation: fadeIn 1s ease-in;
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(-10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .tagline {
        font-size: 1.5rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        animation: slideIn 0.8s ease-out 0.3s both;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .container {
            padding: 1rem;
        }
        
        .ascii-logo {
            font-size: 0.5rem;
        }
        
        .tagline {
            font-size: 1.1rem;
        }
    }
</style>
<div class="container" style="text-align: center;">
    <pre class="ascii-logo" style="color: whitesmoke !important; background-color: transparent !important; font-family: monospace !important; line-height: 1.0 !important; display: inline-block; text-align: left;">

    ██████╗ ███████╗███████╗██████╗  ██████╗ ██╗  ██╗███████╗███╗   ██╗
    ██╔══██╗██╔════╝██╔════╝██╔══██╗██╔═══██╗██║ ██╔╝██╔════╝████╗  ██║
    ██████╔╝█████╗  ███████╗██████╔╝██║   ██║█████╔╝ █████╗  ██╔██╗ ██║
    ██╔══██╗██╔══╝  ╚════██║██╔═══╝ ██║   ██║██╔═██╗ ██╔══╝  ██║╚██╗██║
    ██████╔╝███████╗███████║██║     ╚██████╔╝██║  ██╗███████╗██║ ╚████║
    ╚═════╝ ╚══════╝╚══════╝╚═╝      ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝

   Define your agent. Pick your tools. Add your commands. Make it your own.
    </pre>
</div>


# What is Bespoken?

Bespoken is a framework that allows you to create custom LLM agents for the command line. 

<div style="text-align: center;">
    <pre class="ascii-logo" style="color: whitesmoke !important; background-color: transparent !important; font-family: monospace !important; line-height: 1.2 !important;">
┌───────┐  ┌───────┐  ┌──────┐  ┌───────┐     ┌─────────────────────┐
│ Tools │ +│  LLM  │ +│  UI  │ +│ Cmds  │  =  │    Custom Agent     │
└───────┘  └───────┘  └──────┘  └───────┘     └─────────────────────┘
    </pre>
</div>

You're able to pick your favourite LLM and combine it with your own tools and commands. We also offer a simple UI framework to allow for dynamic forms with auto-completion. All of this is wrapped in a single command line utility that covers enough ground to get you started on your own bespoke agent.

## Why build this?

It all started when I was working with claude code and found myself constantly telling it that it was only allow to make changes to a specific file. Similarily, I wanted to be able to make commits from within the chat interface without wasting tokens. It turned into a fun evening and before I knew it I had built myself a flexible framework on top of [llm](https://llm.datasette.io/en/stable/). 

<!-- ![intro](static/intro.svg) -->

## Quickstart

If you want to use `bespoken` you'll want to install it first. 

```bash
uv pip install bespoken
```

From here, the easiest way to explain how `bespoken` works is to show you an example. 

```python title="app.py"
from bespoken import chat
from bespoken.tools import FileTool, TodoTools
from bespoken import ui

def set_role():
    """Set a voice for the assistant"""
    roles = ["pirate", "teacher", "professor"]
    role = ui.choice("What role should I take?", roles)
    return f"You are now speaking like a {role}. Please respond in character for this role."

chat(
    model_name="anthropic/claude-3-5-sonnet-20240620",
    tools=[FileTool("edit.py"), TodoTools()],
    system_prompt="You are a helpful assistant.",
    debug=False,
    slash_commands={
        "/role": set_role,
    }
)
```

You can run this app via `uv run app.py` and you will get an agent. 

The agent is basically a while loop that keeps on asking for input and the LLM will call tools when it deems it appropriate. This experience is constrained and bespoke to your needs because you fully control what tools are available to the LLM. Depending on what commands you give the LLM  it will pick up the `FileTool` or `TodoTools` to call the tools on your behalf. The `FileTool` can read/edit a specific file and the `TodoTools` can keep track of an internal todo list. 

You're also able to add commands to the agent that you can trigger yourself. In this example we added the `/role` command that allows you to change the role of the assistant. You'll also notice that we're adding a system prompt that you can also customise. 

## How does it work?

Bespoken builds on top of the [llm](https://llm.datasette.io/en/stable/) tool created by [Simon Willison](https://simonwillison.net/). This gives us ample LLMs to pick from, some of which support "tools".

> Tools are a way to give an LLM the ability to perform actions on your behalf. You can define these as normal Python functions/classes. If you give these good names and docstrings, the LLM can call them when it deems it appropriate and can interpret the output. This library provides you with plenty of tools out of the box, but you can also define your own. The whole point is that you only give the LLM access to the tools it needs to perform its task and nothing more, as a guardrail.

Besides tools this library also allows you to customise the system prompt and you can also define "slash commands". 

> Slash commands are a way to give an LLM the ability to perform actions on your behalf. Unlike a tool, the LLM does not trigger it, you do! Some of these commands are pre-defined prompts that you like to use while debugging while others might allow you to make a commit manually from within the chat interface (that way you won't waste precious tokens). We ship with some pre-defined commands but the whole point is that you can also configure your own. 

One of the main features of `bespoken` is that we also allow you to use `bespoken.ui` to enhance these tools and commands. 

> When the `FileTool` is about to make a change to a file, it will confirm if you agree to the change. To make this nice it is calling `bespoken.ui.confirm()` internally and depending on what the user returns the LLM will branch off to a different state. You can add these UI steps in your tools but also in your slash commands as you see fit. Besides ui, we also offer some shortcuts like `@<filename>` that all benefit from autocompletion too.

We also allow you to change the basics like the system prompt and the base model. Bespoken also comes with debugging tools to figure out what the tools are doing while you interact with the LLM. 

## Next steps?

This is about the gist of it. The project is in it's early stages right now and we're mainly interested in gathering feedback. We could make it look nicer, add more tools, more prompts or more commands, probably add a good callback system for logging/debugging ... but before doing that we'd like to make sure that our pipeline is flexible enough to cover the needs of a general crowd. So let us know! 

You can find the source code on [github](https://github.com/koaning/bespoken) and we'd love to hear from you!
