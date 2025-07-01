import llm
import questionary
import typer
from dotenv import load_dotenv
from rich import print
from rich.console import Console
from rich.spinner import Spinner
from rich.live import Live

from . import config
from .config import custom_style_fancy
from .tools import FileTools


load_dotenv(".env")


def chat(
    debug: bool = typer.Option(False, "--debug", "-d", help="Enable debug mode to see LLM interactions"),
    model_name: str = typer.Option("anthropic/claude-3-5-sonnet-20240620", "--model", "-m", help="LLM model to use"),
):
    """Run the bespoken chat assistant."""
    # Set debug mode globally
    config.DEBUG_MODE = debug
    
    if debug:
        print("[magenta]Debug mode enabled[/magenta]\n")
    
    console = Console()
    
    try:
        model = llm.get_model(model_name)
    except Exception as e:
        print(f"[red]Error loading model '{model_name}': {e}[/red]")
        raise typer.Exit(1)
    
    conversation = model.conversation(tools=[FileTools()])
    
    print("[cyan]Welcome to Bespoken! Type 'quit' to exit.[/cyan]\n")
    
    try:
        while True:
            out = questionary.text("", qmark=">", style=custom_style_fancy).ask()
            if out == "quit":
                break
            # Show spinner while getting initial response
            spinner = Spinner("dots", text="[dim]Thinking...[/dim]")
            response_started = False
            
            with Live(spinner, console=console, refresh_per_second=10) as live:
                for chunk in conversation.chain(out, system="You are a coding assistant that can make edits to a single file. In particular you will make edits to a marimo notebook."):
                    if not response_started:
                        # First chunk received, stop the spinner
                        live.stop()
                        response_started = True
                        if config.DEBUG_MODE:
                            print("\n[magenta]>>> LLM Response:[/magenta]\n")
                    print(f"[dim]{chunk}[/dim]", end="", flush=True)
            print()
    except KeyboardInterrupt:
        print("\n\n[cyan]Thanks for using Bespoken. Goodbye![/cyan]\n")


def main():
    """Main entry point for the bespoken CLI."""
    typer.run(chat)


if __name__ == "__main__":
    main()
