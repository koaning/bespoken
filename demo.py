from textual.app import App, ComposeResult
from textual.widgets import Input, Static, Label, Footer, ListView, ListItem, Markdown
from textual.containers import Container, VerticalScroll, Horizontal
from textual.events import Key
from textual.screen import ModalScreen
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

class CommandPalette(ModalScreen):
    """A custom command palette modal."""
    
    BINDINGS = [("escape", "dismiss", "Close")]
    
    def compose(self) -> ComposeResult:
        with Container(id="command-palette"):
            yield Input(
                placeholder="Type to search commands...",
                id="command-search"
            )
            yield ListView(
                ListItem(Label("🎨 Theme: Dark"), id="theme-dark"),
                ListItem(Label("🎨 Theme: Light"), id="theme-light"),
                ListItem(Label("🎨 Theme: Dracula"), id="theme-dracula"),
                ListItem(Label("🎨 Theme: Nord"), id="theme-nord"),
                ListItem(Label("🎨 Theme: Gruvbox"), id="theme-gruvbox"),
                ListItem(Label("🎨 Theme: Monokai"), id="theme-monokai"),
                ListItem(Label("🎨 Theme: Solarized Light"), id="theme-solarized-light"),
                ListItem(Label("🎨 Theme: Solarized Dark"), id="theme-solarized-dark"),
                ListItem(Label("❌ Clear Output"), id="cmd-clear"),
                ListItem(Label("❓ Show Help"), id="cmd-help"),
                ListItem(Label("🚪 Quit Application"), id="cmd-quit"),
                id="command-list"
            )
    
    def on_mount(self) -> None:
        """Focus search input when mounted."""
        self.query_one("#command-search").focus()
    
    def on_input_changed(self, event: Input.Changed) -> None:
        """Filter commands based on search input."""
        search_term = event.value.lower()
        list_view = self.query_one("#command-list")
        
        for item in list_view.children:
            if isinstance(item, ListItem):
                label_text = item.query_one(Label).renderable.plain.lower()
                item.display = search_term in label_text if search_term else True
    
    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Execute the selected command."""
        command_id = event.item.id
        
        if command_id.startswith("theme-"):
            theme_name = command_id.replace("theme-", "")
            self.apply_theme(theme_name)
        elif command_id == "cmd-clear":
            self.clear_output()
        elif command_id == "cmd-help":
            self.show_help()
        elif command_id == "cmd-quit":
            self.app.exit()
        
        self.dismiss()
    
    def apply_theme(self, theme_name: str) -> None:
        """Apply the selected theme."""
        self.app.dark = True
        
        if theme_name == "light":
            self.app.dark = False
        elif theme_name == "solarized-light":
            self.app.dark = False
            self.app.theme = "solarized-light"
        else:
            self.app.theme = theme_name
    
    def clear_output(self) -> None:
        """Clear the output container."""
        self.app.markdown_output.update("**Output cleared!**")
    
    def show_help(self) -> None:
        """Show help message in output."""
        help_text = """\n\n## Available shortcuts:
- **Ctrl+K**: Open command palette
- **@ + filename**: Autocomplete files
- **/ + command**: Autocomplete commands
- **Ctrl+C**: Quit application"""
        self.app.markdown_output.append(help_text)
        output = self.app.query_one("#output-container")
        output.anchor()


class DynamicDataApp(App[None]):
    BINDINGS = [
        ("ctrl+k", "open_command_palette", "Command Palette"),
    ]
    
    CSS = """
    #output-container {
        height: 1fr;
        padding: 1;
        align-vertical: bottom;
    }
    
    #input-container {
        height: 3;
        dock: bottom;
        margin-bottom: 2;
    }
    
    Input {
        dock: bottom;
        border: solid $surface-lighten-1;
        padding: 0 1;
        margin: 0 1;
    }
    
    Input:focus {
        border: solid $surface-lighten-2;
    }
    
    
    Horizontal {
        height: 3;
    }
    
    .user-message {
        color: $primary;
        margin-bottom: 1;
    }
    
    .bot-message {
        color: $success;
        margin-bottom: 1;
    }
    
    #command-palette {
        width: 60;
        height: 80%;
        max-height: 30;
        background: $surface;
        border: thick $primary;
        padding: 1;
    }
    
    #command-search {
        margin-bottom: 1;
        width: 100%;
    }
    
    #command-list {
        height: 1fr;
        background: $panel;
    }
    
    #command-list > ListItem {
        padding: 0 1;
    }
    
    #command-list > ListItem.--highlight {
        background: $primary 20%;
    }
    """
    
    def compose(self) -> ComposeResult:
        # Output area at the top
        with VerticalScroll(id="output-container"):
            pass  # Start empty, welcome message will be added in on_mount
        
        # Input area at the bottom
        with Container(id="input-container"):
            with Horizontal():
                input_widget = Input(placeholder="Type @ for files, / for commands...", id="chat-input")
                yield input_widget
                self.autocomplete = CustomAutoComplete(input_widget, candidates=self.candidates_callback)
                yield self.autocomplete
        
        # Footer showing command palette shortcut
        yield Footer()

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

    def on_mount(self) -> None:
        """Focus the input when the app starts"""
        # Add welcome message using a single Markdown widget
        output_container = self.query_one("#output-container")
        self.markdown_output = Markdown("**Welcome!** Try typing `@` for files or `/` for commands. Press `Ctrl+K` for command palette.")
        output_container.mount(self.markdown_output)
        
        # Focus the input
        self.query_one("#chat-input").focus()
    
    def action_open_command_palette(self) -> None:
        """Open the custom command palette."""
        self.push_screen(CommandPalette())
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle when user presses Enter"""
        if not event.value:
            return
        
        # Add user message and bot response using markdown.append
        user_message = f"\n\n**You:** {event.value}"
        bot_response = f"\n\n**Bot:** {event.value}"
        
        self.markdown_output.append(user_message)
        self.markdown_output.append(bot_response)
        
        # Clear input
        event.input.value = ""
        
        # Anchor to bottom so it sticks as content is added
        output_container = self.query_one("#output-container")
        output_container.anchor()
    
    def on_key(self, event: Key) -> None:
        # Handle Ctrl+C to quit
        if event.key == "ctrl+c":
            self.exit()


if __name__ == "__main__":
    app = DynamicDataApp()
    app.run()