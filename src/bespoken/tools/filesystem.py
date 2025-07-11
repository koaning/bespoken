"""File tools for the bespoken assistant."""

from typing import Optional
from pathlib import Path
import difflib
import re
import llm
from rich import get_console
from rich.prompt import Confirm, Prompt

from .. import ui


class FileSystem(llm.Toolbox):
    """File system operations toolbox - can work with multiple files and directories."""
    
    def __init__(self, working_directory: str = "."):
        self.working_directory = Path(working_directory).resolve()
    
    def _debug_return(self, value: str) -> str:
        """Helper to show what the LLM receives from tools"""
        ui.tool_debug(f"\n>>> Tool returning to LLM: {repr(value)}\n")
        return value
        
    def _resolve_path(self, file_path: str) -> Path:
        if Path(file_path).is_absolute():
            return Path(file_path).resolve()
        return (self.working_directory / file_path).resolve()
    
    def list_files(self, directory: Optional[str] = None) -> str:
        """List files and directories."""
        ui.tool_debug(f">>> LLM calling tool: list_files(directory={repr(directory)})")
        ui.tool_status(f"Listing files in {directory or 'current directory'}...")
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
        ui.tool_debug(f">>> LLM calling tool: read_file(file_path={repr(file_path)})")
        ui.tool_status(f"Reading file: {file_path}")
        full_path = self._resolve_path(file_path)
        content = full_path.read_text(encoding='utf-8', errors='replace')
        
        if len(content) > 50_000:
            content = content[:50_000] + "\n... (truncated)"
            
        return self._debug_return(content)
    
    def write_file(self, file_path: str, content: str) -> str:
        """Write content to a file."""
        ui.tool_debug(f">>> LLM calling tool: write_file(file_path={repr(file_path)}, content=<{len(content)} chars>)")
        ui.tool_status(f"Writing {len(content):,} characters to: {file_path}")
        full_path = self._resolve_path(file_path)
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content, encoding='utf-8')
        
        return self._debug_return(f"Wrote {len(content):,} characters to '{file_path}'")
    
    def replace_in_file(self, file_path: str, old_string: str, new_string: str) -> str:
        """Replace string in file and show diff. The user may deny the change, in which case you should wait for new instructions."""
        ui.tool_debug(f">>> LLM calling tool: replace_in_file(file_path={repr(file_path)}, old_string=<{len(old_string)} chars>, new_string=<{len(new_string)} chars>)")
        ui.tool_status(f"Preparing to replace text in: {file_path}")
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
            ui.tool_warning("Proposed changes:")
            ui.print("")
            
            # Parse the diff to add line numbers and colors
            line_num_old = 0
            line_num_new = 0
            
            for line in diff_lines:
                if line.startswith('---') or line.startswith('+++'):
                    # File headers
                    ui.print(f"[dim]{line.rstrip()}[/dim]")
                elif line.startswith('@@'):
                    # Hunk header - extract line numbers
                    match = re.search(r'-(\d+)(?:,\d+)? \+(\d+)(?:,\d+)?', line)
                    if match:
                        line_num_old = int(match.group(1))
                        line_num_new = int(match.group(2))
                    ui.print(f"[cyan]{line.rstrip()}[/cyan]")
                elif line.startswith('-'):
                    # Removed line
                    ui.print(f"[on red][white]{line_num_old:4d} {line.rstrip()}[/white][/on red]")
                    line_num_old += 1
                elif line.startswith('+'):
                    # Added line
                    ui.print(f"[on green][white]{line_num_new:4d} {line.rstrip()}[/white][/on green]")
                    line_num_new += 1
                elif line.startswith(' '):
                    # Context line
                    ui.print(f"[dim]{line_num_old:4d}[/dim] {line.rstrip()}")
                    line_num_old += 1
                    line_num_new += 1
                else:
                    # Other lines (shouldn't happen in unified diff)
                    ui.print(line.rstrip())
            
            ui.print("")  # Extra newline for clarity
            
            # Ask for confirmation
            ui.print_empty_line()  # Empty line for clarity
            confirm = ui.confirm(
                "Apply these changes?", 
                default=True
            )
            
            if confirm:
                full_path.write_text(new_content, encoding='utf-8')
                return self._debug_return(f"Applied changes to '{file_path}'")
            else:
                ui.tool_error("Changes cancelled. Please provide new instructions.")
                return self._debug_return("IMPORTANT: The user declined the changes. Do not continue with the task. Wait for new instructions from the user. IMPORTANT: Do not continue with the task.")
        else:
            return self._debug_return(f"No changes needed in '{file_path}'")


def FileTool(file_path: Optional[str] = None):
    """Factory function to create a FileTool with file-specific docstring."""
    if file_path is None:
        file_path = ui.input("Enter the path to the file you want to edit: ")
    
    file_path_obj = Path(file_path).resolve()
    if not file_path_obj.exists():
        raise FileNotFoundError(f"File does not exist: {file_path}")
    
    class _FileTool(llm.Toolbox):
        f"""Single file editing toolbox - focused on editing {file_path_obj.name}. This tool cannot be used to open or edit other files."""
        
        def __init__(self):
            self.file_path = file_path_obj
        
        def _debug_return(self, value: str) -> str:
            """Helper to show what the LLM receives from tools"""
            ui.tool_debug(f"\n>>> Tool returning to LLM: {value}\n")
            return value
        
        def get_file_path(self) -> str:
            """Return the path to the file that this tool is allowed to edit."""
            ui.tool_debug(">>> LLM calling tool: get_file_path()")
            ui.tool_status(f"Getting file path for: {self.file_path.name}")
            return self._debug_return(f"This tool can only access one file: {self.file_path}. Other files exist but are not accessible through this tool.")
        
        def read_file(self) -> str:
            f"""Read the content of {self.file_path.name}. This tool cannot be used to open or edit other files."""
            ui.tool_debug(">>> LLM calling tool: read_file()")
            ui.tool_status(f"Reading file: {self.file_path.name}")
            
            content = self.file_path.read_text(encoding='utf-8', errors='replace')
            
            if len(content) > 50_000:
                content = content[:50_000] + "\n... (truncated)"
                
            return self._debug_return(content)
        
        def replace_in_file(self, old_string: str, new_string: str) -> str:
            f"""Replace string in {self.file_path.name} and show diff. The user may deny the change, in which case you should wait for new instructions. This tool cannot be used to open or edit other files."""
            ui.tool_debug(f">>> LLM calling tool: replace_in_file(old_string=<{len(old_string)} chars>, new_string=<{len(new_string)} chars>)")
            ui.tool_status(f"Preparing to replace text in: {self.file_path.name}")
            
            original_content = self.file_path.read_text(encoding='utf-8')
            new_content = original_content.replace(old_string, new_string)
            
            diff_lines = list(difflib.unified_diff(
                original_content.splitlines(keepends=True),
                new_content.splitlines(keepends=True),
                fromfile=f"{self.file_path.name} (before)",
                tofile=f"{self.file_path.name} (after)",
                n=3
            ))
            
            if diff_lines:
                # Show the diff with custom formatting
                ui.tool_warning("Proposed changes:")
                ui.print_empty_line()
                
                # Parse the diff to add line numbers and colors
                line_num_old = 0
                line_num_new = 0
                
                for line in diff_lines:
                    if line.startswith('---') or line.startswith('+++'):
                        # File headers
                        ui.print(f"[dim]{line.rstrip()}[/dim]")
                    elif line.startswith('@@'):
                        # Hunk header - extract line numbers
                        match = re.search(r'-(\d+)(?:,\d+)? \+(\d+)(?:,\d+)?', line)
                        if match:
                            line_num_old = int(match.group(1))
                            line_num_new = int(match.group(2))
                        ui.print(f"[cyan]{line.rstrip()}[/cyan]")
                    elif line.startswith('-'):
                        # Removed line
                        ui.print(f"[on red][white]{line_num_old:4d} {line.rstrip()}[/white][/on red]")
                        line_num_old += 1
                    elif line.startswith('+'):
                        # Added line
                        ui.print(f"[on green][white]{line_num_new:4d} {line.rstrip()}[/white][/on green]")
                        line_num_new += 1
                    elif line.startswith(' '):
                        # Context line
                        ui.print(f"[dim]{line_num_old:4d}[/dim] {line.rstrip()}")
                        line_num_old += 1
                        line_num_new += 1
                    else:
                        # Other lines (shouldn't happen in unified diff)
                        ui.print(line.rstrip())
                
                ui.print("")  # Extra newline for clarity
                
                # Ask for confirmation
                ui.print_empty_line()  # Empty line for clarity
                confirm = ui.confirm(
                    "Apply these changes?", 
                    default=True
                )
                
                if confirm:
                    self.file_path.write_text(new_content, encoding='utf-8')
                    return self._debug_return(f"Applied changes to '{self.file_path.name}'")
                else:
                    ui.tool_error("Changes cancelled. Please provide new instructions.")
                    return self._debug_return("IMPORTANT: The user declined the changes. Do not continue with the task. Wait for new instructions from the user. IMPORTANT: Do not continue with the task.")
            else:
                return self._debug_return(f"No changes needed in '{self.file_path.name}'")
    
    return _FileTool()