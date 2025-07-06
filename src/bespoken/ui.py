"""User interface utilities for consistent formatting in bespoken."""

from typing import List, Any, Optional
from rich.console import Console
from rich.prompt import Prompt, Confirm

try:
    from prompt_toolkit import prompt
    from prompt_toolkit.completion import WordCompleter
    from prompt_toolkit.styles import Style
    from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
    from prompt_toolkit.history import InMemoryHistory
    from prompt_toolkit.formatted_text import HTML
    from .file_completer import create_completer
    PROMPT_TOOLKIT_AVAILABLE = True
except ImportError:
    PROMPT_TOOLKIT_AVAILABLE = False


# Global padding configuration
LEFT_PADDING = 2
RIGHT_PADDING = 2

# Private console instance - all output must go through this module
_console = Console()

# Default ASCII art for bespoken
_DEFAULT_ASCII_ART = """██████╗ ███████╗███████╗██████╗  ██████╗ ██╗  ██╗███████╗███╗   ██╗
██╔══██╗██╔════╝██╔════╝██╔══██╗██╔═══██╗██║ ██╔╝██╔════╝████╗  ██║
██████╔╝█████╗  ███████╗██████╔╝██║   ██║█████╔╝ █████╗  ██╔██╗ ██║
██╔══██╗██╔══╝  ╚════██║██╔═══╝ ██║   ██║██╔═██╗ ██╔══╝  ██║╚██╗██║
██████╔╝███████╗███████║██║     ╚██████╔╝██║  ██╗███████╗██║ ╚████║
╚═════╝ ╚══════╝╚══════╝╚═╝      ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝"""

_DEFAULT_SUBTITLE = """[dim]A terminal chat experience that you can configure yourself.[/dim]
[cyan]Type 'quit' to exit.[/cyan]"""

# Custom ASCII art storage
_custom_ascii_art = None
_custom_subtitle = None

# Trust settings for tools
_trusted_tools = set()

# Command history for prompt_toolkit
_command_history = InMemoryHistory() if PROMPT_TOOLKIT_AVAILABLE else None


def print(text: str, indent: int = LEFT_PADDING) -> None:
    """Print text with left padding."""
    # For single line text, just add padding
    if '\n' not in text:
        _console.print(" " * indent + text)
        return
    
    # For multi-line text, split and add padding to each line
    lines = text.split('\n')
    for line in lines:
        _console.print(" " * indent + line)


def stream(chunks, indent: int = LEFT_PADDING, wrap: bool = True) -> None:
    """Stream text chunks with word-aware wrapping and padding."""
    # State for word-aware wrapping
    current_position = 0
    word_buffer = ""
    terminal_width = _console.width
    max_line_width = terminal_width - indent - RIGHT_PADDING
    at_line_start = True
    
    for chunk in chunks:
        # Process chunk character by character
        for char in chunk:
            if at_line_start:
                # Add padding at start of line
                _console.print(" " * indent, end="", highlight=False)
                at_line_start = False
                current_position = 0
            
            if char == '\n':
                # Print any buffered word
                if word_buffer:
                    _console.print(f"[dim]{word_buffer}[/dim]", end="", highlight=False)
                    word_buffer = ""
                # New line
                _console.print()
                at_line_start = True
            elif char in ' \t' and wrap:
                # End of word, check if it fits
                if word_buffer:
                    word_length = len(word_buffer)
                    if current_position + word_length > max_line_width:
                        # Word doesn't fit, wrap to new line
                        _console.print()
                        at_line_start = True
                        _console.print(" " * indent, end="", highlight=False)
                        current_position = 0
                        at_line_start = False
                    # Print the word
                    _console.print(f"[dim]{word_buffer}[/dim]", end="", highlight=False)
                    current_position += word_length
                    word_buffer = ""
                # Print the space
                _console.print(f"[dim]{char}[/dim]", end="", highlight=False)
                current_position += 1
            else:
                # Add to word buffer
                word_buffer += char
    
    # Print any remaining buffered word
    if word_buffer:
        if wrap and current_position + len(word_buffer) > max_line_width:
            _console.print()
            at_line_start = True
            _console.print(" " * indent, end="", highlight=False)
        _console.print(f"[dim]{word_buffer}[/dim]", end="", highlight=False)


def input(prompt_text: str, indent: int = LEFT_PADDING, completions: Optional[List[str]] = None) -> str:
    """Get input with left padding and optional completions."""
    padded_prompt = " " * indent + prompt_text
    
    if completions and PROMPT_TOOLKIT_AVAILABLE:
        # Use combined completer for commands and file paths
        completer = create_completer(completions)
        
        if completer:
            # Create a style with auto-suggestion preview in gray
            style = Style.from_dict({
                # Default text style
                '': '#ffffff',
                # Auto-suggestions in gray
                'auto-suggest': 'fg:#666666',
                # Selected completion in menu
                'completion-menu.completion.current': 'bg:#00aaaa #000000',
                'completion-menu.completion': 'bg:#008888 #ffffff',
            })
            
            try:
                # Use prompt_toolkit with completer and auto-suggestions
                result = prompt(
                    padded_prompt,
                    completer=completer,
                    style=style,
                    complete_while_typing=True,  # Show completions as you type
                    auto_suggest=AutoSuggestFromHistory(),  # Suggest from history
                    history=_command_history,  # Enable history with up/down arrows
                    enable_history_search=False,  # Disable Ctrl+R search
                )
                return result
            except (KeyboardInterrupt, EOFError):
                raise KeyboardInterrupt()
    else:
        # Fall back to Rich console input
        return _console.input(padded_prompt)


def confirm(prompt: str, indent: int = LEFT_PADDING, default: bool = True) -> bool:
    """Ask for confirmation with left padding."""
    # Add padding to the prompt
    padded_prompt = " " * indent + prompt
    return Confirm.ask(padded_prompt, default=default, console=_console)


def choice(prompt: str, choices: List[str], indent: int = LEFT_PADDING) -> str:
    """Present a choice menu with left padding."""
    # Add padding to the prompt
    padded_prompt = " " * indent + prompt
    return Prompt.ask(padded_prompt, choices=choices, console=_console)


def set_ascii_art(ascii_art: str, subtitle: str = None) -> None:
    """Set custom ASCII art and optional subtitle for the banner."""
    global _custom_ascii_art, _custom_subtitle
    _custom_ascii_art = ascii_art
    _custom_subtitle = subtitle


def show_banner() -> None:
    """Display the ASCII art banner with padding."""
    # Determine which art and subtitle to use
    ascii_art = _custom_ascii_art if _custom_ascii_art is not None else _DEFAULT_ASCII_ART
    subtitle = _custom_subtitle if _custom_subtitle is not None else _DEFAULT_SUBTITLE
    
    padding = " " * LEFT_PADDING
    
    # Build the complete banner
    banner_lines = []
    banner_lines.append(f"{padding}[bold cyan]")
    
    # Add ASCII art lines
    for line in ascii_art.split('\n'):
        banner_lines.append(f"{padding}{line}")
    
    banner_lines.append(f"{padding}[/bold cyan]")
    banner_lines.append("")  # Empty line
    
    # Add subtitle lines
    for line in subtitle.split('\n'):
        banner_lines.append(f"{padding}{line}")
    
    # Print the banner
    _console.print()  # Add space before banner
    _console.print('\n'.join(banner_lines))


def trust_tool(tool_name: str) -> None:
    """Mark a tool as trusted (no confirmation needed)."""
    _trusted_tools.add(tool_name)


def untrust_tool(tool_name: str) -> None:
    """Remove a tool from the trusted list."""
    _trusted_tools.discard(tool_name)


def is_tool_trusted(tool_name: str) -> bool:
    """Check if a tool is trusted."""
    return tool_name in _trusted_tools


def confirm_tool_action(tool_name: str, action_description: str, details: dict = None, default: bool = True) -> bool:
    """Confirm a tool action, respecting trust settings."""
    # If tool is trusted, auto-confirm
    if is_tool_trusted(tool_name):
        print(f"[dim]Auto-executing trusted tool: {tool_name}[/dim]")
        return True
    
    # Otherwise, show details and ask for confirmation
    print(f"[bold yellow]Tool: {tool_name}[/bold yellow]")
    print(f"[bold]Action:[/bold] {action_description}")
    
    if details:
        for key, value in details.items():
            if value:  # Only show non-empty values
                print(f"[bold]{key}:[/bold] {value}")
    
    return confirm(f"Execute this {tool_name} action?", default=default)