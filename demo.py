from textual.app import App, ComposeResult
from textual.widgets import Input
from textual.events import Key
from pathlib import Path
import os

from textual_autocomplete import AutoComplete
from textual_autocomplete._autocomplete import DropdownItem, TargetState


class CustomAutoComplete(AutoComplete):
    def get_search_string(self, state: TargetState) -> str:
        # Get the last word including special prefixes like @ or /
        text = state.text
        cursor_pos = state.cursor_position
        
        # Find the start of the current word (look backwards for space)
        word_start = cursor_pos
        while word_start > 0 and text[word_start - 1] not in ' \t\n':
            word_start -= 1
        
        # Return the word from start to cursor position
        return text[word_start:cursor_pos]
    
    def should_show_dropdown(self, search_string: str) -> bool:
        """Always show dropdown when we have candidates"""
        # Show dropdown when:
        # 1. Search string contains @ (file paths)
        # 2. Search string starts with / (commands)  
        # 3. Search string ends with / (directory navigation)
        should_show = "@" in search_string or search_string.startswith("/") or search_string.endswith("/")
        
        # If we should show and we're at a directory boundary, make sure dropdown is visible
        if should_show and search_string.endswith("/") and hasattr(self, '_dropdown'):
            self.call_later(lambda: self.action_show())
            
        return should_show

    def apply_completion(self, value: str, state: TargetState) -> None:
        """Replace the current word with the selected completion"""
        text = state.text
        cursor_pos = state.cursor_position
        
        # Find the start of the current word (look backwards for space or start of string)
        word_start = cursor_pos
        while word_start > 0 and text[word_start - 1] not in ' \t\n':
            word_start -= 1
        
        # Find the end of the current word (look forwards for space or end of string)
        word_end = cursor_pos
        while word_end < len(text) and text[word_end] not in ' \t\n':
            word_end += 1
        
        # Replace the current word with the completion
        new_text = text[:word_start] + value + text[word_end:]
        new_cursor_pos = word_start + len(value)
        
        # Update the input
        self.target.value = new_text
        self.target.cursor_position = new_cursor_pos
        
        # Rebuild the dropdown with the new state
        new_target_state = self._get_target_state()
        search_string = self.get_search_string(new_target_state)
        self._rebuild_options(new_target_state, search_string)
        
        # If we just completed a directory (ends with /), force refresh the dropdown
        if value.endswith("/"):
            # Force the autocomplete to update with the new directory contents
            self.call_after_refresh(self._handle_target_update)

class DynamicDataApp(App[None]):
    def compose(self) -> ComposeResult:
        input_widget = Input()
        yield input_widget
        self.autocomplete = CustomAutoComplete(input_widget, candidates=self.candidates_callback)
        yield self.autocomplete

    def candidates_callback(self, state: TargetState) -> list[DropdownItem]:
        # Get the current word at cursor position
        text = state.text
        cursor_pos = state.cursor_position
        
        # Find the start of the current word
        word_start = cursor_pos
        while word_start > 0 and text[word_start - 1] not in ' \t\n':
            word_start -= 1
        
        current_word = text[word_start:cursor_pos]
        
        # Check if we're looking for file paths
        if current_word.startswith("@"):
            return self.get_file_candidates(current_word[1:])  # Remove @ prefix
        
        # Check if we're looking for commands
        elif current_word.startswith("/"):
            return self.get_command_candidates(current_word)
        
        # Otherwise return empty list (no suggestions for regular words in this example)
        return []
    
    def get_command_candidates(self, prefix: str) -> list[DropdownItem]:
        """Get command candidates that start with the given prefix"""
        all_commands = [
            "/quit",
            "/start", 
            "/stop",
            "/help",
            "/clear",
            "/status"
        ]
        
        filtered = [cmd for cmd in all_commands if cmd.startswith(prefix)]
        return [DropdownItem(cmd, prefix="📝 ") for cmd in filtered]
    
    def get_file_candidates(self, partial_path: str) -> list[DropdownItem]:
        """Get file/directory candidates based on partial path"""
        print(f"DEBUG: Getting file candidates for: '{partial_path}'")
        try:
            # Handle cases like "src/" where we want contents of src
            if partial_path.endswith("/"):
                base_dir = partial_path.rstrip("/") if partial_path.rstrip("/") else "."
                prefix = ""
            elif not partial_path:
                base_dir = "."
                prefix = ""
            else:
                # Split into directory and partial filename
                if "/" in partial_path:
                    base_dir = os.path.dirname(partial_path)
                    prefix = os.path.basename(partial_path)
                else:
                    base_dir = "."
                    prefix = partial_path
            
            # Get all items in the directory
            items = []
            base_path = Path(base_dir)
            
            if base_path.exists() and base_path.is_dir():
                for item in base_path.iterdir():
                    if prefix and not item.name.startswith(prefix):
                        continue
                    
                    # Build the path relative to current directory
                    if partial_path and "/" in partial_path:
                        # Keep the directory part
                        rel_path = os.path.join(os.path.dirname(partial_path), item.name)
                    else:
                        rel_path = item.name
                    
                    # Add @ prefix back and indicate if it's a directory
                    if item.is_dir():
                        items.append(DropdownItem(f"@{rel_path}/", prefix="📁 "))
                    else:
                        items.append(DropdownItem(f"@{rel_path}", prefix="📄 "))
            
            return sorted(items, key=lambda x: x.value)[:20]  # Limit to 20 results
            
        except (OSError, PermissionError):
            return []

    def on_key(self, event: Key) -> None:
        # Handle Ctrl+C to quit
        if event.key == "ctrl+c":
            self.exit()


if __name__ == "__main__":
    app = DynamicDataApp()
    app.run()