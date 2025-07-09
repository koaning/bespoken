# Overview

Bespoken is built on several core concepts that work together to provide a powerful LLM-powered CLI experience:

## Key Concepts

### 1. LLM Interaction

Bespoken uses the [llm](https://llm.datasette.io/en/stable/) library from Simon Willison to interact with various LLM providers. This gives you access to models from Anthropic, OpenAI, and others, including local models.

### 2. Tool System

The tool system allows you to define specific capabilities that the LLM can access, constraining its actions to only what you explicitly permit.

### 3. Slash Commands

Slash commands provide user-triggered actions that can be executed during a conversation, enhancing the interactive experience.

### 4. UI Components

Bespoken includes a set of UI components that make the CLI experience more interactive and user-friendly.

## Architecture

```
┌─────────────────┐     ┌──────────────┐     ┌───────────────────┐
│  User Interface │────>│  Bespoken    │────>│  LLM Integration  │
└─────────────────┘     └──────────────┘     └───────────────────┘
                              │
                              │
                        ┌─────┴──────┐
                        │   Tools    │
                        └────────────┘
```

This architecture allows Bespoken to be both powerful and extensible while maintaining a simple interface for users.
