from datetime import datetime
from typing import Any, Dict, List

import llm
from rich import print

from .. import config


class TodoTools(llm.Toolbox):
    """Todo management toolbox."""
    
    def __init__(self):
        self._todos: List[Dict[str, Any]] = []
    
    def _debug_return(self, value: str) -> str:
        """Helper to show what the LLM receives from tools"""
        config.tool_debug(f"\n>>> Tool returning to LLM: {repr(value)}\n")
        return value
            
    def add_todo(self, task: str) -> str:
        """Add a new todo item."""
        config.tool_debug(f">>> LLM calling tool: add_todo(task={repr(task)})")
        config.tool_status(f"Adding todo: {task}")
        
        self._todos.append({
            "task": task,
            "done": False,
            "created": datetime.now().isoformat()
        })
        
        return self._debug_return(f"Added todo: '{task}'")
    
    def list_todos(self) -> str:
        """List all todos with their status."""
        config.tool_debug(">>> LLM calling tool: list_todos()")
        config.tool_status("Listing todos...")
        
        if not self._todos:
            return self._debug_return("No todos found. Add one with add_todo()")
            
        lines = ["Todo List:"]
        for i, todo in enumerate(self._todos):
            status = "✓" if todo.get("done", False) else "○"
            lines.append(f"{i + 1}. [{status}] {todo['task']}")
            
        return self._debug_return("\n".join(lines))
    
    def mark_todo_done(self, index: int) -> str:
        """Mark a todo as completed."""
        config.tool_debug(f">>> LLM calling tool: mark_todo_done(index={repr(index)})")
        config.tool_status(f"Marking todo #{index} as done...")
        
        todo = self._todos[index - 1]
        todo["done"] = True
        todo["completed"] = datetime.now().isoformat()
        
        return self._debug_return(f"Marked as done: '{todo['task']}'")
    
    def flush_todos(self) -> str:
        """Flush all todos."""
        config.tool_debug(">>> LLM calling tool: flush_todos()")
        config.tool_status("Flushing all todos...")
        
        self._todos.clear()
        return self._debug_return("Flushed todos. All todos have been deleted.")