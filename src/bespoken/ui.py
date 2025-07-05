"""User interface utilities for consistent formatting in bespoken."""

from typing import List, Optional, Any
from rich.console import Console
from rich.prompt import Prompt, Confirm


# Global padding configuration
LEFT_PADDING = 2
RIGHT_PADDING = 2


def print(text: str, indent: int = LEFT_PADDING, console: Optional[Console] = None) -> None:
    """Print text with left padding."""
    if console is None:
        console = Console()
    
    # For single line text, just add padding
    if '\n' not in text:
        console.print(" " * indent + text)
        return
    
    # For multi-line text, split and add padding to each line
    lines = text.split('\n')
    for line in lines:
        console.print(" " * indent + line)


def stream(chunks, indent: int = LEFT_PADDING, wrap: bool = True, console: Optional[Console] = None) -> None:
    """Stream text chunks with word-aware wrapping and padding."""
    if console is None:
        console = Console()
    
    # State for word-aware wrapping
    current_position = 0
    word_buffer = ""
    terminal_width = console.width
    max_line_width = terminal_width - indent - RIGHT_PADDING
    at_line_start = True
    
    for chunk in chunks:
        # Process chunk character by character
        for char in chunk:
            if at_line_start:
                # Add padding at start of line
                console.print(" " * indent, end="", highlight=False)
                at_line_start = False
                current_position = 0
            
            if char == '\n':
                # Print any buffered word
                if word_buffer:
                    console.print(f"[dim]{word_buffer}[/dim]", end="", highlight=False)
                    word_buffer = ""
                # New line
                console.print()
                at_line_start = True
            elif char in ' \t' and wrap:
                # End of word, check if it fits
                if word_buffer:
                    word_length = len(word_buffer)
                    if current_position + word_length > max_line_width:
                        # Word doesn't fit, wrap to new line
                        console.print()
                        at_line_start = True
                        console.print(" " * indent, end="", highlight=False)
                        current_position = 0
                        at_line_start = False
                    # Print the word
                    console.print(f"[dim]{word_buffer}[/dim]", end="", highlight=False)
                    current_position += word_length
                    word_buffer = ""
                # Print the space
                console.print(f"[dim]{char}[/dim]", end="", highlight=False)
                current_position += 1
            else:
                # Add to word buffer
                word_buffer += char
    
    # Print any remaining buffered word
    if word_buffer:
        if wrap and current_position + len(word_buffer) > max_line_width:
            console.print()
            at_line_start = True
            console.print(" " * indent, end="", highlight=False)
        console.print(f"[dim]{word_buffer}[/dim]", end="", highlight=False)


def input(prompt: str, indent: int = LEFT_PADDING, console: Optional[Console] = None) -> str:
    """Get input with left padding."""
    if console is None:
        console = Console()
    
    return console.input(" " * indent + prompt)


def confirm(prompt: str, indent: int = LEFT_PADDING, default: bool = True, console: Optional[Console] = None) -> bool:
    """Ask for confirmation with left padding."""
    if console is None:
        console = Console()
    
    # Add padding to the prompt
    padded_prompt = " " * indent + prompt
    return Confirm.ask(padded_prompt, default=default, console=console)


def choice(prompt: str, choices: List[str], indent: int = LEFT_PADDING, console: Optional[Console] = None) -> str:
    """Present a choice menu with left padding."""
    if console is None:
        console = Console()
    
    # Add padding to the prompt
    padded_prompt = " " * indent + prompt
    return Prompt.ask(padded_prompt, choices=choices, console=console)