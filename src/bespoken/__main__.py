from typing import Optional

import llm
import typer
from dotenv import load_dotenv
from rich import print
from rich.console import Console
from rich.spinner import Spinner
from rich.live import Live
from rich.prompt import Prompt
from rich.columns import Columns
from rich.text import Text

from . import config
from . import ui


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
    
    console = Console()

        # ASCII art welcome
    padding = " " * ui.LEFT_PADDING
    ascii_art = f"""{padding}[bold cyan]
{padding}██████╗ ███████╗███████╗██████╗  ██████╗ ██╗  ██╗███████╗███╗   ██╗
{padding}██╔══██╗██╔════╝██╔════╝██╔══██╗██╔═══██╗██║ ██╔╝██╔════╝████╗  ██║
{padding}██████╔╝█████╗  ███████╗██████╔╝██║   ██║█████╔╝ █████╗  ██╔██╗ ██║
{padding}██╔══██╗██╔══╝  ╚════██║██╔═══╝ ██║   ██║██╔═██╗ ██╔══╝  ██║╚██╗██║
{padding}██████╔╝███████╗███████║██║     ╚██████╔╝██║  ██╗███████╗██║ ╚████║
{padding}╚═════╝ ╚══════╝╚══════╝╚═╝      ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝
{padding}[/bold cyan]

{padding}[dim]A terminal chat experience that you can configure yourself.[/dim]
{padding}[cyan]Type 'quit' to exit.[/cyan]"""
    
    print()  # Add space before ASCII art
    console.print(ascii_art)
    
    if debug:
        ui.print("[magenta]Debug mode enabled[/magenta]")
        print()
    
    try:
        model = llm.get_model(model_name)
    except Exception as e:
        ui.print(f"[red]Error loading model '{model_name}': {e}[/red]")
        raise typer.Exit(1)
    
    conversation = model.conversation(tools=tools)
    
    try:
        while True:
            out = ui.input("[bold]> [/bold]")
            if out == "quit":
                break
            
            print()  # Add whitespace before thinking spinner
            # Show spinner while getting initial response
            # Create a padded spinner
            spinner_text = Text("Thinking...", style="dim")
            padded_spinner = Columns([Text(" " * ui.LEFT_PADDING), Spinner("dots"), spinner_text], expand=False)
            response_started = False
            
            with Live(padded_spinner, console=console, refresh_per_second=10) as live:
                response_chunks = []
                for chunk in conversation.chain(out, system=system_prompt):
                    if not response_started:
                        # First chunk received, stop the spinner
                        live.stop()
                        response_started = True
                        print()  # Add whitespace after spinner
                        if config.DEBUG_MODE:
                            ui.print("[magenta]>>> LLM Response:[/magenta]")
                            print()
                    response_chunks.append(chunk)
                
                # Stream the response with padding and wrapping
                ui.stream(response_chunks)
            print("\n")  # Add extra newline after bot response
    except KeyboardInterrupt:
        print("\n")  # Add newlines
        ui.print("[cyan]Thanks for using Bespoken. Goodbye![/cyan]")
        print()  # Add final newline


def main():
    """Main entry point for the bespoken CLI."""
    typer.run(chat)


if __name__ == "__main__":
    main()
