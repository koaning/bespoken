from typing import Optional
import llm
import questionary
from questionary import Style
from dotenv import load_dotenv
from pathlib import Path
from rich import print


load_dotenv(".env")


class CallTool(BaseModel):
    should_call: bool
    reasoning: str


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

model = llm.get_model("claude-3.7-sonnet")

def upper(text: str) -> str:
    "convert text to upper case"
    return text.upper()

def reverse(text: str) -> str:
    "reverse text"
    return text[::-1]

def ls(folder: Optional[str] = None) -> str:
    """Show the files in the current directory."""
    return "\n".join([str(_) for _ in Path(folder or ".").glob("*")])

def ask_preference(options: list[str]) -> str:
    """Choose an option from a list."""
    return questionary.select(
        "Choose an option",
        choices=options,
        style=custom_style_fancy,
    ).ask()

conversation = model.conversation(tools=[ls, upper, reverse, ask_preference])

while True:
    out = questionary.text("", qmark=">", style=custom_style_fancy).ask()
    if out == "quit":
        break
    out = f"The user said: {out}. Should the assistant use the tools? If so, call the tool. If not, just respond to the user."
    response = conversation.chain(out)

    for chunk in response:
        print(chunk, end="", flush=True)
    print()