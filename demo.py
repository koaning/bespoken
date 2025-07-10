from textual.app import App, ComposeResult
from textual.widgets import Input
from textual.events import Key

from textual_autocomplete import AutoComplete
from textual_autocomplete._autocomplete import DropdownItem, TargetState


class CustomAutoComplete(AutoComplete):
    def get_search_string(self, state: TargetState) -> str:
        return state.text.split(" ")[-1]
    
    def apply_candidates(self, state: TargetState) -> None:
        self.candidates = self.candidates_callback(state)
        self.dropdown.candidates = self.candidates
        self.dropdown.show()

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
        self._rebuild_options(
            new_target_state, self.get_search_string(new_target_state)
        )

class DynamicDataApp(App[None]):
    def compose(self) -> ComposeResult:
        input_widget = Input()
        yield input_widget
        yield CustomAutoComplete(input_widget, candidates=self.candidates_callback)

    def candidates_callback(self, state: TargetState) -> list[DropdownItem]:
        # Get the current word being typed
        current_word = state.text.split(" ")[-1] if state.text else ""
        
        # All available completions
        all_candidates = [
            "/quit",
            "/start", 
            "/stop",
            "/help",
            "@foobar",
            "@foobar2",
            "Apple",
            "Banana", 
            "Cherry",
            "Orange"
        ]
        
        # Filter candidates based on what's being typed
        if current_word:
            filtered = [item for item in all_candidates if item.startswith(current_word)]
        else:
            filtered = all_candidates
        
        return [
            DropdownItem(item, prefix="📝 " if item.startswith("/") else "🍎 " if not item.startswith("@") else "📁 ")
            for item in filtered
        ]

    def on_key(self, event: Key) -> None:
        # Handle Ctrl+C to quit
        if event.key == "ctrl+c":
            self.exit()


if __name__ == "__main__":
    app = DynamicDataApp()
    app.run()