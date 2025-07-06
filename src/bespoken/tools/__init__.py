"""Tools for the bespoken assistant."""

from .filesystem import FileSystem, FileTool
from .todo import TodoTools
from .webfetch import WebFetchTool
from ..not_installed import NotInstalled

try:
    from .playwright_browser import PlaywrightTool
except ImportError:
    # Replace with NotInstalled proxy
    PlaywrightTool = NotInstalled("PlaywrightTool", "browser")



__all__ = ["FileSystem", "FileTool", "TodoTools", "WebFetchTool", "PlaywrightTool"]