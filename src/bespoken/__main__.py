import typer
from typing import Optional
import llm
import questionary
from questionary import Style
from dotenv import load_dotenv
from pathlib import Path
from rich import print
from rich.console import Console
from rich.spinner import Spinner
from rich.live import Live
import difflib
import threading


load_dotenv(".env")

# Debug mode - set to True to see LLM's perspective
DEBUG_MODE = False

custom_style_fancy = Style([
    ('qmark', 'fg:#673ab7 bold'),       # token in front of the question
    ('question', 'bold'),               # question text
    ('answer', 'fg:#154a57'),      # submitted answer text behind the question
    ('pointer', 'fg:#673ab7 bold'),     # pointer used in select and checkbox prompts
    ('highlighted', 'fg:#673ab7 bold'), # pointed-at choice in select and checkbox prompts
    ('selected', 'fg:#154a57'),         # style for a selected item of a checkbox
    ('separator', 'fg:#154a57'),        # separator in lists
    ('instruction', ''),                # user instructions for select, rawselect, checkbox
    ('text', ''),                       # plain text
    ('disabled', 'fg:#858585 italic')   # disabled choices for select and checkbox prompts
])

class FileTools(llm.Toolbox):
    """File operations toolbox."""
    
    def __init__(self, working_directory: str = "."):
        self.working_directory = Path(working_directory).resolve()
    
    def _debug_return(self, value: str) -> str:
        """Helper to show what the LLM receives from tools"""
        if DEBUG_MODE:
            print(f"\n[magenta]>>> Tool returning to LLM: {repr(value)}[/magenta]\n")
        return value
        
    def _resolve_path(self, file_path: str) -> Path:
        if Path(file_path).is_absolute():
            return Path(file_path).resolve()
        return (self.working_directory / file_path).resolve()
    
    def list_files(self, directory: Optional[str] = None) -> str:
        """List files and directories."""
        if DEBUG_MODE:
            print(f"\n[magenta]>>> LLM calling tool: list_files(directory={repr(directory)})[/magenta]")
        print()  # Ensure we start on a new line
        print(f"[cyan]Listing files in {directory or 'current directory'}...[/cyan]")
        print()
        target_dir = self._resolve_path(directory) if directory else self.working_directory
        
        items = []
        for item in sorted(target_dir.iterdir()):
            if item.is_dir():
                items.append(f"{item.name}/ [DIR]")
            else:
                items.append(f"{item.name} ({item.stat().st_size} bytes)")
                
        return self._debug_return(f"Files in {target_dir}:\n" + "\n".join(items) if items else "No files found")
    
    def read_file(self, file_path: str) -> str:
        """Read content from a file."""
        if DEBUG_MODE:
            print(f"\n[magenta]>>> LLM calling tool: read_file(file_path={repr(file_path)})[/magenta]")
        print()  # Ensure we start on a new line
        print(f"[cyan]Reading file: {file_path}[/cyan]")
        print()
        full_path = self._resolve_path(file_path)
        content = full_path.read_text(encoding='utf-8', errors='replace')
        
        if len(content) > 50_000:
            content = content[:50_000] + "\n... (truncated)"
            
        return self._debug_return(content)
    
    def write_file(self, file_path: str, content: str) -> str:
        """Write content to a file."""
        if DEBUG_MODE:
            print(f"\n[magenta]>>> LLM calling tool: write_file(file_path={repr(file_path)}, content=<{len(content)} chars>)[/magenta]")
        print()  # Ensure we start on a new line
        print(f"[cyan]Writing {len(content):,} characters to: {file_path}[/cyan]")
        print()
        full_path = self._resolve_path(file_path)
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content, encoding='utf-8')
        
        return self._debug_return(f"Wrote {len(content):,} characters to '{file_path}'")
    
    def replace_in_file(self, file_path: str, old_string: str, new_string: str) -> str:
        """Replace string in file and show diff. The user may deny the change, in which case you should wait for new instructions."""
        if DEBUG_MODE:
            print(f"\n[magenta]>>> LLM calling tool: replace_in_file(file_path={repr(file_path)}, old_string=<{len(old_string)} chars>, new_string=<{len(new_string)} chars>)[/magenta]")
        print()  # Ensure we start on a new line
        print(f"[cyan]Preparing to replace text in: {file_path}[/cyan]")
        print()
        full_path = self._resolve_path(file_path)
        original_content = full_path.read_text(encoding='utf-8')
        new_content = original_content.replace(old_string, new_string)
        
        diff_lines = list(difflib.unified_diff(
            original_content.splitlines(keepends=True),
            new_content.splitlines(keepends=True),
            fromfile=f"{file_path} (before)",
            tofile=f"{file_path} (after)",
            n=3
        ))
        
        if diff_lines:
            # Show the diff with custom formatting
            print("[yellow]Proposed changes:[/yellow]")
            print()
            
            # Parse the diff to add line numbers and colors
            line_num_old = 0
            line_num_new = 0
            
            for line in diff_lines:
                if line.startswith('---') or line.startswith('+++'):
                    # File headers
                    print(f"[dim]{line.rstrip()}[/dim]")
                elif line.startswith('@@'):
                    # Hunk header - extract line numbers
                    import re
                    match = re.search(r'-(\d+)(?:,\d+)? \+(\d+)(?:,\d+)?', line)
                    if match:
                        line_num_old = int(match.group(1))
                        line_num_new = int(match.group(2))
                    print(f"[cyan]{line.rstrip()}[/cyan]")
                elif line.startswith('-'):
                    # Removed line
                    print(f"[on red][white]{line_num_old:4d} {line.rstrip()}[/white][/on red]")
                    line_num_old += 1
                elif line.startswith('+'):
                    # Added line
                    print(f"[on green][white]{line_num_new:4d} {line.rstrip()}[/white][/on green]")
                    line_num_new += 1
                elif line.startswith(' '):
                    # Context line
                    print(f"[dim]{line_num_old:4d}[/dim] {line.rstrip()}")
                    line_num_old += 1
                    line_num_new += 1
                else:
                    # Other lines (shouldn't happen in unified diff)
                    print(line.rstrip())
            
            print()  # Extra newline for clarity
            
            # Ask for confirmation
            from rich import get_console
            get_console().print()  # Force flush any pending output
            confirm = questionary.confirm(
                "Apply these changes?", 
                default=True,
                style=custom_style_fancy
            ).ask()
            
            if confirm:
                full_path.write_text(new_content, encoding='utf-8')
                return self._debug_return(f"Applied changes to '{file_path}'")
            else:
                print("\n[red]Changes cancelled. Please provide new instructions.[/red]\n")
                return self._debug_return("IMPORTANT: The user declined the changes. Do not continue with the task. Wait for new instructions from the user. IMPORTANT: Do not continue with the task.")
        else:
            return self._debug_return(f"No changes needed in '{file_path}'")


def main():
    """Main entry point for the bespoken CLI."""
    console = Console()
    model = llm.get_model("anthropic/claude-3-5-sonnet-20240620")
    
    conversation = model.conversation(tools=[FileTools()])
    
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
                    print(f"[dim]{chunk}[/dim]", end="", flush=True)
            print()
    except KeyboardInterrupt:
        print("\n\n[cyan]Thanks for using the chat assistant. Goodbye![/cyan]\n")


if __name__ == "__main__":
    main()
