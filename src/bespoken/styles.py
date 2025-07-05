"""Predefined visual styles for bespoken."""

from typing import Dict, Optional
from . import ui


# Style definitions
STYLES = {
    "default": {
        "name": "Default",
        "ascii_art": """██████╗ ███████╗███████╗██████╗  ██████╗ ██╗  ██╗███████╗███╗   ██╗
██╔══██╗██╔════╝██╔════╝██╔══██╗██╔═══██╗██║ ██╔╝██╔════╝████╗  ██║
██████╔╝█████╗  ███████╗██████╔╝██║   ██║█████╔╝ █████╗  ██╔██╗ ██║
██╔══██╗██╔══╝  ╚════██║██╔═══╝ ██║   ██║██╔═██╗ ██╔══╝  ██║╚██╗██║
██████╔╝███████╗███████║██║     ╚██████╔╝██║  ██╗███████╗██║ ╚████║
╚═════╝ ╚══════╝╚══════╝╚═╝      ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝""",
        "subtitle": "[dim]A terminal chat experience that you can configure yourself.[/dim]\n[cyan]Type 'quit' to exit.[/cyan]",
        "theme": "default"
    },
    
    "minimal": {
        "name": "Minimal",
        "ascii_art": "bespoken",
        "subtitle": "[dim]chat assistant[/dim]",
        "theme": "minimal"
    },
    
    "hacker": {
        "name": "Hacker",
        "ascii_art": """╔╗ ╔═╗╔═╗╔═╗╔═╗╦╔═╔═╗╔╗╔
╠╩╗║╣ ╚═╗╠═╝║ ║╠╩╗║╣ ║║║
╚═╝╚═╝╚═╝╩  ╚═╝╩ ╩╚═╝╝╚╝""",
        "subtitle": "[green]> system ready[/green]\n[green]> type 'quit' to terminate[/green]",
        "theme": "hacker"
    },
    
    "professional": {
        "name": "Professional",
        "ascii_art": """BESPOKEN
Professional Edition""",
        "subtitle": "[blue]Enterprise Chat Assistant[/blue]\n[dim]Type 'quit' to exit session[/dim]",
        "theme": "professional"
    },
    
    "fun": {
        "name": "Fun",
        "ascii_art": """┌─┐┬ ┬┌─┐┌┬┐  ┌┬┐┬┌┬┐┌─┐
│  ├─┤├─┤ │    │ ││││├┤ 
└─┘┴ ┴┴ ┴ ┴    ┴ ┴┴ ┴└─┘""",
        "subtitle": "[magenta]✨ Let's chat! ✨[/magenta]\n[yellow]Type 'quit' when you're done[/yellow]",
        "theme": "fun"
    }
}


def apply_style(style_name: str) -> bool:
    """Apply a predefined style. Returns True if successful."""
    if style_name not in STYLES:
        return False
    
    style = STYLES[style_name]
    ui.set_ascii_art(style["ascii_art"], style["subtitle"])
    
    # Could also set color themes, padding, etc. here in the future
    return True


def list_styles() -> Dict[str, str]:
    """Return available styles with their descriptions."""
    return {name: style["name"] for name, style in STYLES.items()}


def get_style_preview(style_name: str) -> Optional[str]:
    """Get a preview of what a style looks like."""
    if style_name not in STYLES:
        return None
    
    style = STYLES[style_name]
    preview = f"=== {style['name']} Style ===\n\n"
    preview += style["ascii_art"] + "\n\n"
    preview += style["subtitle"]
    return preview