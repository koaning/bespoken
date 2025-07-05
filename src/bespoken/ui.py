"""User interface utilities for consistent formatting in bespoken."""

from typing import List, Any
from rich.console import Console
from rich.prompt import Prompt, Confirm


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


def input(prompt: str, indent: int = LEFT_PADDING) -> str:
    """Get input with left padding."""
    return _console.input(" " * indent + prompt)


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