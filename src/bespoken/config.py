"""Configuration settings for bespoken."""

from rich import print

# Import padding constant to avoid circular imports
LEFT_PADDING = 2

# Debug mode - set to True to see LLM's perspective
DEBUG_MODE = False


def tool_status(message: str) -> None:
    """Print a tool status message in cyan."""
    print("\n")  # Add extra whitespace before tool message
    print(f"{' ' * LEFT_PADDING}[cyan]{message}[/cyan]")
    print()


def tool_debug(message: str) -> None:
    """Print a debug message in magenta (only when DEBUG_MODE is True)."""
    if DEBUG_MODE:
        # Handle multiline messages by adding padding to each line
        lines = message.split('\n')
        for line in lines:
            print(f"{' ' * LEFT_PADDING}[magenta]{line}[/magenta]")


def tool_error(message: str) -> None:
    """Print an error message in red."""
    print(f"{' ' * LEFT_PADDING}[red]{message}[/red]")


def tool_success(message: str) -> None:
    """Print a success message in green."""
    print(f"{' ' * LEFT_PADDING}[green]{message}[/green]")


def tool_warning(message: str) -> None:
    """Print a warning message in yellow."""
    print(f"{' ' * LEFT_PADDING}[yellow]{message}[/yellow]")