"""Bespoken - An AI-powered coding assistant for editing files with interactive confirmations."""

import importlib.metadata

from .__main__ import chat

# Get version dynamically from package metadata
try:
    __version__ = importlib.metadata.version("bespoken")
except:
    __version__ = "unknown"

__all__ = ["chat", "__version__"]