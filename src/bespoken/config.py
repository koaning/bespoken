"""Configuration settings for bespoken."""

# Import padding constant to avoid circular imports
LEFT_PADDING = 2

# Debug mode - set to True to see LLM's perspective
DEBUG_MODE = True

# Backward compatibility imports - these functions have moved to ui module
from .ui import tool_status, tool_debug, tool_error, tool_success, tool_warning