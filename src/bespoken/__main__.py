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


def handle_quit():
    """Handle /quit command"""
    return "QUIT"


def handle_help(user_commands):
    """Handle /help command"""
    ui.print("[cyan]Built-in commands:[/cyan]")
    ui.print("  /quit   - Exit the application")
    ui.print("  /help   - Show this help message")
    ui.print("  /tools  - Show available tools")
    ui.print("  /debug  - Toggle debug mode")
    
    if user_commands:
        ui.print("")
        ui.print("[cyan]Custom commands:[/cyan]")
        for cmd_name, cmd_handler in user_commands.items():
            if callable(cmd_handler):
                desc = cmd_handler.__doc__ or "Custom function"
                ui.print(f"  {cmd_name}   - {desc}")
            else:
                preview = str(cmd_handler)[:50] + "..." if len(str(cmd_handler)) > 50 else str(cmd_handler)
                ui.print(f"  {cmd_name}   - {preview}")
    
    ui.print("")
    return "HANDLED"




def handle_tools(tools):
    """Handle /tools command"""
    if tools:
        ui.print("[cyan]Available tools:[/cyan]")
        for tool in tools:
            tool_name = getattr(tool, 'tool_name', type(tool).__name__)
            ui.print(f"  {tool_name}")
    else:
        ui.print("[dim]No tools configured[/dim]")
    ui.print("")
    return "HANDLED"


def toggle_debug():
    """Toggle debug mode on/off"""
    config.DEBUG_MODE = not config.DEBUG_MODE
    status = "enabled" if config.DEBUG_MODE else "disabled"
    ui.print(f"[magenta]Debug mode {status}[/magenta]")
    ui.print("")
    return "HANDLED"


def handle_user_command(command, handler):
    """Handle user-defined command"""
    try:
        if callable(handler):
            result = handler()
            if result:
                if isinstance(result, str):
                    # If it looks like a message for the LLM, send it
                    if not result.startswith("[") and not result.endswith("]"):
                        return result  # Treat as LLM input
                    else:
                        # Treat as UI message
                        ui.print(result)
                        ui.print("")
                        return "HANDLED"
                else:
                    ui.print(str(result))
                    ui.print("")
                    return "HANDLED"
            else:
                return "HANDLED"
        else:
            # String - send directly to LLM
            return str(handler)
    except Exception as e:
        ui.print(f"[red]Error executing command {command}: {e}[/red]")
        ui.print("")
        return "HANDLED"


def dispatch_slash_command(command, user_commands, model, tools, conversation):
    """Dispatch slash command to appropriate handler"""
    if command == "/quit":
        return handle_quit(), conversation
    elif command == "/help":
        return handle_help(user_commands), conversation
    elif command == "/tools":
        return handle_tools(tools), conversation
    elif command == "/debug":
        return toggle_debug(), conversation
    elif command in user_commands:
        return handle_user_command(command, user_commands[command]), conversation
    else:
        ui.print(f"[red]Unknown command: {command}[/red]")
        ui.print("[dim]Type /help for available commands[/dim]")
        ui.print("")
        return "HANDLED", conversation


def chat(
    debug: bool = typer.Option(False, "--debug", "-d", help="Enable debug mode to see LLM interactions"),
    model_name: str = typer.Option("anthropic/claude-3-5-sonnet-20240620", "--model", "-m", help="LLM model to use"),
    system_prompt: Optional[str] = typer.Option(None, "--system", "-s", help="System prompt for the assistant"),
    tools: list = None,
    slash_commands: dict = None,
):
    """Run the bespoken chat assistant."""
    # Set debug mode globally
    config.DEBUG_MODE = debug
    
    # Initialize user slash commands
    user_commands = slash_commands or {}
    
    console = Console()

    # Show the banner
    ui.show_banner()
    
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
            # Define available commands for completion (builtin + user commands)
            builtin_commands = ["/quit", "/help", "/tools", "/debug"]
            user_command_names = list(user_commands.keys())
            completions = builtin_commands + user_command_names
            
            # Show completion hint on first prompt
            if not hasattr(chat, '_shown_completion_hint'):
                ui.print("[dim]Tips: TAB for completions • @file.py for file paths • ↑/↓ for history • Ctrl+U to clear[/dim]")
                chat._shown_completion_hint = True
            
            out = ui.input("> ", completions=completions).strip()
            
            # Handle slash commands
            if out.startswith("/"):
                result, conversation = dispatch_slash_command(out, user_commands, model, tools, conversation)
                
                if result == "QUIT":
                    break
                elif result == "HANDLED":
                    continue
                else:
                    # Command returned text for LLM
                    out = result
            
            # Skip empty input
            if not out.strip():
                continue
            
            print()  # Add whitespace before thinking spinner
            # Show spinner while getting initial response
            # Create a padded spinner
            spinner_text = Text("Thinking...", style="dim")
            padded_spinner = Columns([Text(" " * ui.LEFT_PADDING), Spinner("dots"), spinner_text], expand=False)
            response_started = False
            
            with Live(padded_spinner, console=console, refresh_per_second=10) as live:
                for chunk in conversation.chain(out, system=system_prompt):
                    if not response_started:
                        # First chunk received, stop the spinner
                        live.stop()
                        response_started = True
                        print()  # Add whitespace after spinner
                        if config.DEBUG_MODE:
                            ui.print("[magenta]>>> LLM Response:[/magenta]")
                            print()
                        # Initialize streaming state
                        ui.start_streaming()
                    
                    # Stream each chunk as it arrives
                    ui.stream_chunk(chunk)
                
                # Finish streaming and print any remaining text
                if response_started:
                    ui.end_streaming()
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
