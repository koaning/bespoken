"""File path completion for @ references in bespoken."""

import os
from pathlib import Path
from typing import Iterable, List

from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.document import Document


class FilePathCompleter(Completer):
    """Completer for file paths after @ symbol."""
    
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path).resolve()
    
    def get_completions(self, document: Document, complete_event) -> Iterable[Completion]:
        """Generate file path completions after @ symbol."""
        text = document.text_before_cursor
        
        # Find the last @ symbol and extract the path after it
        at_pos = text.rfind('@')
        if at_pos == -1:
            return
        
        # Get the partial path after @
        path_part = text[at_pos + 1:]
        
        # If there's a space after @, we're not completing a path anymore
        if ' ' in path_part and not path_part.endswith(' '):
            return
        
        # Remove any trailing space
        path_part = path_part.rstrip()
        
        try:
            # Resolve the path relative to base_path
            if path_part:
                search_path = self.base_path / path_part
                if search_path.is_file():
                    # If it's already a complete file, no more completions
                    return
                elif search_path.is_dir():
                    # Complete contents of directory
                    search_dir = search_path
                    prefix = path_part + "/"
                else:
                    # Partial path - complete from parent directory
                    search_dir = search_path.parent
                    prefix = str(search_path.parent.relative_to(self.base_path))
                    if prefix != ".":
                        prefix += "/"
                    else:
                        prefix = ""
            else:
                # Just @ - complete from base directory
                search_dir = self.base_path
                prefix = ""
            
            if not search_dir.exists():
                return
            
            # Get all files and directories in the search directory
            items = []
            try:
                for item in search_dir.iterdir():
                    if item.name.startswith('.'):
                        continue  # Skip hidden files
                    
                    relative_path = item.relative_to(self.base_path)
                    completion_text = str(relative_path)
                    
                    # Only include items that start with our current path part
                    if path_part and not completion_text.startswith(path_part):
                        continue
                    
                    # Calculate what to insert (the part after what's already typed)
                    if path_part:
                        insert_text = completion_text[len(path_part):]
                    else:
                        insert_text = completion_text
                    
                    # Add / for directories
                    display_text = completion_text
                    if item.is_dir():
                        display_text += "/"
                        if not insert_text.endswith("/"):
                            insert_text += "/"
                    
                    items.append((insert_text, display_text))
                
                # Sort items (directories first, then files)
                items.sort(key=lambda x: (not x[1].endswith("/"), x[1].lower()))
                
                # Yield completions
                for insert_text, display_text in items:
                    yield Completion(
                        text=insert_text,
                        display=display_text,
                        start_position=0
                    )
                    
            except PermissionError:
                # Skip directories we can't read
                pass
                
        except (OSError, ValueError):
            # Handle invalid paths gracefully
            pass


class CombinedCompleter(Completer):
    """Completer that handles both commands and file paths."""
    
    def __init__(self, commands: List[str], base_path: str = "."):
        self.commands = commands
        self.file_completer = FilePathCompleter(base_path)
    
    def get_completions(self, document: Document, complete_event) -> Iterable[Completion]:
        """Generate completions for commands or file paths."""
        text = document.text_before_cursor
        
        # Check if we're completing a file path (contains @)
        if '@' in text:
            yield from self.file_completer.get_completions(document, complete_event)
        else:
            # Complete commands at the beginning of input
            words = text.split()
            if len(words) <= 1:
                # Complete commands
                current_word = words[0] if words else ""
                for command in self.commands:
                    if command.startswith(current_word):
                        yield Completion(
                            text=command[len(current_word):],
                            display=command,
                            start_position=0
                        )


def create_completer(commands: List[str], base_path: str = "."):
    """Create a combined completer for commands and file paths."""
    return CombinedCompleter(commands, base_path)