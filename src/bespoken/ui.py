"""User interface utilities for consistent formatting in bespoken."""

from typing import List, Any, Optional
from rich.console import Console
from rich.prompt import Prompt, Confirm

from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter, FuzzyCompleter
from prompt_toolkit.styles import Style
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.formatted_text import HTML
import questionary
from .file_completer import create_completer


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

# Get version dynamically to avoid circular import
def _get_version():
    """Get version without circular import."""
    try:
        import importlib.metadata
        return importlib.metadata.version("bespoken")
    except:
        return "unknown"

_DEFAULT_SUBTITLE = f"""[dim]bespoken v{_get_version()} - A terminal chat experience that you can configure yourself.[/dim]"""

# Custom ASCII art storage
_custom_ascii_art = None
_custom_subtitle = None

# Trust settings for tools
_trusted_tools = set()

# Command history for prompt_toolkit
_command_history = InMemoryHistory()

# Global streaming state
_streaming_state = {
    'current_position': 0,
    'word_buffer': '',
    'at_line_start': True,
    'terminal_width': 0,
    'max_line_width': 0
}


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


def print_empty_line(indent: int = LEFT_PADDING) -> None:
    """Print an empty line with padding to maintain consistent left margin."""
    _console.print(" " * indent)


def print_neutral(text: str, indent: int = LEFT_PADDING) -> None:
    """Print text in neutral gray color with proper padding and wrapping."""
    # Use the streaming infrastructure to handle padding correctly
    start_streaming(indent)
    stream_chunk(text, indent)
    end_streaming(indent)
    print_empty_line(indent)  # Add newline after the text with padding


def tool_status(message: str, indent: int = LEFT_PADDING) -> None:
    """Print a tool status message in cyan."""
    _console.print()  # Add extra whitespace before tool message
    _console.print(f"{' ' * indent}[cyan]{message}[/cyan]")
    _console.print()


def tool_debug(message: str, indent: int = LEFT_PADDING) -> None:
    """Print a debug message in magenta (only when DEBUG_MODE is True)."""
    from . import config
    if config.DEBUG_MODE:
        # Handle multiline messages by adding padding to each line
        lines = message.split('\n')
        for line in lines:
            _console.print(f"{' ' * indent}[magenta]{line}[/magenta]")


def tool_error(message: str, indent: int = LEFT_PADDING) -> None:
    """Print an error message in red."""
    _console.print(f"{' ' * indent}[red]{message}[/red]")


def tool_success(message: str, indent: int = LEFT_PADDING) -> None:
    """Print a success message in green."""
    _console.print(f"{' ' * indent}[green]{message}[/green]")


def tool_warning(message: str, indent: int = LEFT_PADDING) -> None:
    """Print a warning message in yellow."""
    _console.print(f"{' ' * indent}[yellow]{message}[/yellow]")


def start_streaming(indent: int = LEFT_PADDING) -> None:
    """Initialize streaming state."""
    global _streaming_state
    _streaming_state['current_position'] = 0
    _streaming_state['word_buffer'] = ''
    _streaming_state['at_line_start'] = True
    _streaming_state['terminal_width'] = _console.width
    _streaming_state['max_line_width'] = _streaming_state['terminal_width'] - indent - RIGHT_PADDING


def stream_chunk(chunk: str, indent: int = LEFT_PADDING, wrap: bool = True) -> None:
    """Stream a single chunk while maintaining state."""
    global _streaming_state
    
    # Process chunk character by character
    for char in chunk:
        if _streaming_state['at_line_start']:
            # Add padding at start of line
            _console.print(" " * indent, end="", highlight=False)
            _streaming_state['at_line_start'] = False
            _streaming_state['current_position'] = 0
        
        if char == '\n':
            # Print any buffered word
            if _streaming_state['word_buffer']:
                _console.print(f"[dim]{_streaming_state['word_buffer']}[/dim]", end="", highlight=False)
                _streaming_state['word_buffer'] = ""
            # New line
            _console.print()
            _streaming_state['at_line_start'] = True
        elif char in ' \t' and wrap:
            # End of word, check if it fits
            if _streaming_state['word_buffer']:
                word_length = len(_streaming_state['word_buffer'])
                if _streaming_state['current_position'] + word_length > _streaming_state['max_line_width']:
                    # Word doesn't fit, wrap to new line
                    _console.print()
                    _streaming_state['at_line_start'] = True
                    _console.print(" " * indent, end="", highlight=False)
                    _streaming_state['current_position'] = 0
                    _streaming_state['at_line_start'] = False
                # Print the word
                _console.print(f"[dim]{_streaming_state['word_buffer']}[/dim]", end="", highlight=False)
                _streaming_state['current_position'] += word_length
                _streaming_state['word_buffer'] = ""
            # Print the space
            _console.print(f"[dim]{char}[/dim]", end="", highlight=False)
            _streaming_state['current_position'] += 1
        else:
            # Add to word buffer
            _streaming_state['word_buffer'] += char


def end_streaming(indent: int = LEFT_PADDING, wrap: bool = True) -> None:
    """Finish streaming and print any remaining buffered word."""
    global _streaming_state
    
    # Print any remaining buffered word
    if _streaming_state['word_buffer']:
        if wrap and _streaming_state['current_position'] + len(_streaming_state['word_buffer']) > _streaming_state['max_line_width']:
            _console.print()
            _streaming_state['at_line_start'] = True
            _console.print(" " * indent, end="", highlight=False)
        _console.print(f"[dim]{_streaming_state['word_buffer']}[/dim]", end="", highlight=False)


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
    
    # Use combined completer for commands and file paths
    completer = create_completer(completions) if completions else None
    
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


def confirm(prompt: str, indent: int = LEFT_PADDING, default: bool = True) -> bool:
    """Ask for confirmation with left padding."""
    # Add padding to the prompt
    padded_prompt = " " * indent + prompt
    return Confirm.ask(padded_prompt, default=default, console=_console)


def choice(prompt_text: str, choices: List[str], indent: int = LEFT_PADDING) -> str:
    """Present choices using questionary select."""
    # Add blank line before the choice
    print("")
    
    # Add padding to the prompt
    padded_prompt = " " * indent + prompt_text
    
    try:
        result = questionary.select(
            padded_prompt,
            choices=choices,
            use_shortcuts=True,  # Allow number shortcuts
            qmark=""  # Remove the question mark
        ).ask()
        return result or choices[0]  # Default to first choice if cancelled
    except (KeyboardInterrupt, EOFError):
        raise KeyboardInterrupt()


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
        _console.print(f"{' ' * LEFT_PADDING}[dim]Auto-executing trusted tool: {tool_name}[/dim]")
        return True
    
    # Otherwise, show details and ask for confirmation
    _console.print(f"{' ' * LEFT_PADDING}[bold yellow]Tool: {tool_name}[/bold yellow]")
    _console.print(f"{' ' * LEFT_PADDING}[bold]Action:[/bold] {action_description}")
    
    if details:
        for key, value in details.items():
            if value:  # Only show non-empty values
                _console.print(f"{' ' * LEFT_PADDING}[bold]{key}:[/bold] {value}")
    
    return confirm(f"Execute this {tool_name} action?", default=default)