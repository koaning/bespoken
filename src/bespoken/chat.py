"""Chat interface with streaming responses."""

import time
from typing import Iterator, Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.live import Live

app = typer.Typer(help="Bespoken Chat - A beautiful CLI chat interface")


class Chat:
    """A chat interface that repeats user input with streaming effect."""
    
    def __init__(self):
        self.console = Console()
        self.delay = 0.03
    
    def _stream_text(self, text: str, delay: Optional[float] = None) -> Iterator[str]:
        """Stream text character by character."""
        if delay is None:
            delay = self.delay
        for char in text:
            yield char
            time.sleep(delay)
    
    
    def _display_bot_response(self, message: str):
        """Display bot response with streaming effect."""
        self.console.print("[bold green]Bot:[/bold green] ", end="")
        bot_text = Text()
        
        with Live(bot_text, console=self.console, refresh_per_second=30) as live:
            for char in self._stream_text(message):
                bot_text.append(char)
                live.update(bot_text)
    
    def respond(self, user_input: str) -> str:
        """Generate bot response (currently just repeats input)."""
        return f"You said: {user_input}"
    
    def start(self):
        """Start the chat loop."""
        while True:
            try:
                user_input = self.console.input("\n[dim]>[/dim] ")
                
                if user_input.lower() in ['quit', 'exit']:
                    self.console.print(Panel(
                        "[bold yellow]Goodbye![/bold yellow]",
                        border_style="yellow"
                    ))
                    break
                
                if user_input.strip():
                    response = self.respond(user_input)
                    self.console.print("")
                    self._display_bot_response(response)
                
            except KeyboardInterrupt:
                self.console.print("\n[bold red]Chat interrupted.[/bold red]")
                break
            except EOFError:
                break

@app.command()
def chat():
    """Start an interactive chat session."""
    chat_instance = Chat()
    chat_instance.delay = 0.03
    
    chat_instance.start()


def main():
    """Main entry point for the chat CLI."""
    app()


if __name__ == "__main__":
    main()