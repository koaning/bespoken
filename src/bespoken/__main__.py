from typing import Optional

import llm
import typer
from dotenv import load_dotenv
from rich import print
from rich.console import Console
from rich.spinner import Spinner
from rich.live import Live
from rich.prompt import Prompt

from . import config


load_dotenv(".env")


def chat(
    debug: bool = typer.Option(False, "--debug", "-d", help="Enable debug mode to see LLM interactions"),
    model_name: str = typer.Option("anthropic/claude-3-5-sonnet-20240620", "--model", "-m", help="LLM model to use"),
    system_prompt: Optional[str] = typer.Option(None, "--system", "-s", help="System prompt for the assistant"),
    tools: list = None,
):
    """Run the bespoken chat assistant."""
    # Set debug mode globally
    config.DEBUG_MODE = debug

        # ASCII art welcome
    ascii_art = """
[bold cyan]
██████╗ ███████╗███████╗██████╗  ██████╗ ██╗  ██╗███████╗███╗   ██╗
██╔══██╗██╔════╝██╔════╝██╔══██╗██╔═══██╗██║ ██╔╝██╔════╝████╗  ██║
██████╔╝█████╗  ███████╗██████╔╝██║   ██║█████╔╝ █████╗  ██╔██╗ ██║
██╔══██╗██╔══╝  ╚════██║██╔═══╝ ██║   ██║██╔═██╗ ██╔══╝  ██║╚██╗██║
██████╔╝███████╗███████║██║     ╚██████╔╝██║  ██╗███████╗██║ ╚████║
╚═════╝ ╚══════╝╚══════╝╚═╝      ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝
[/bold cyan]

[dim]An AI-powered coding assistant for interactive file editing[/dim]
[cyan]Type 'quit' to exit.[/cyan]
"""
    
    print(ascii_art)
    
    if debug:
        print("[magenta]Debug mode enabled[/magenta]\n")
    
    console = Console()
    
    try:
        model = llm.get_model(model_name)
    except Exception as e:
        print(f"[red]Error loading model '{model_name}': {e}[/red]")
        raise typer.Exit(1)
    
    conversation = model.conversation(tools=tools)
    
    try:
        while True:
            out = Prompt.ask("[bold purple]>[/bold purple]", console=console, default="", show_default=False)
            if out == "quit":
                break
            
            print()  # Add whitespace before thinking spinner
            # Show spinner while getting initial response
            spinner = Spinner("dots", text="[dim]Thinking...[/dim]")
            response_started = False
            
            with Live(spinner, console=console, refresh_per_second=10) as live:
                for chunk in conversation.chain(out, system=system_prompt):
                    if not response_started:
                        # First chunk received, stop the spinner
                        live.stop()
                        response_started = True
                        print()  # Add whitespace after spinner
                        if config.DEBUG_MODE:
                            print("[magenta]>>> LLM Response:[/magenta]\n")
                    print(f"[dim]{chunk}[/dim]", end="", flush=True)
            print("\n")  # Add extra newline after bot response
    except KeyboardInterrupt:
        print("\n\n[cyan]Thanks for using Bespoken. Goodbye![/cyan]\n")


def main():
    """Main entry point for the bespoken CLI."""
    typer.run(chat)


if __name__ == "__main__":
    main()
