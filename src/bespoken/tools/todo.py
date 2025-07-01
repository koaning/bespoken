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
        if config.DEBUG_MODE:
            print(f"\n[magenta]>>> Tool returning to LLM: {repr(value)}[/magenta]\n")
        return value
            
    def add_todo(self, task: str) -> str:
        """Add a new todo item."""
        if config.DEBUG_MODE:
            print(f"\n[magenta]>>> LLM calling tool: add_todo(task={repr(task)})[/magenta]")
        print()  # Ensure we start on a new line
        print(f"[cyan]Adding todo: {task}[/cyan]")
        print()
        
        self._todos.append({
            "task": task,
            "done": False,
            "created": datetime.now().isoformat()
        })
        
        return self._debug_return(f"Added todo: '{task}'")
    
    def list_todos(self) -> str:
        """List all todos with their status."""
        if config.DEBUG_MODE:
            print(f"\n[magenta]>>> LLM calling tool: list_todos()[/magenta]")
        print()  # Ensure we start on a new line
        print(f"[cyan]Listing todos...[/cyan]")
        print()
        
        if not self._todos:
            return self._debug_return("No todos found. Add one with add_todo()")
            
        lines = ["Todo List:"]
        for i, todo in enumerate(self._todos):
            status = "✓" if todo.get("done", False) else "○"
            lines.append(f"{i + 1}. [{status}] {todo['task']}")
            
        return self._debug_return("\n".join(lines))
    
    def mark_todo_done(self, index: int) -> str:
        """Mark a todo as completed."""
        if config.DEBUG_MODE:
            print(f"\n[magenta]>>> LLM calling tool: mark_todo_done(index={repr(index)})[/magenta]")
        print()  # Ensure we start on a new line
        print(f"[cyan]Marking todo #{index} as done...[/cyan]")
        print()
        
        todo = self._todos[index - 1]
        todo["done"] = True
        todo["completed"] = datetime.now().isoformat()
        
        return self._debug_return(f"Marked as done: '{todo['task']}'")
    
    def flush_todos(self) -> str:
        """Flush all todos."""
        if config.DEBUG_MODE:
            print(f"\n[magenta]>>> LLM calling tool: flush_todos()[/magenta]")
        print()  # Ensure we start on a new line
        print(f"[cyan]Flushing all todos...[/cyan]")
        print()
        
        self._todos.clear()
        return self._debug_return("Flushed todos. All todos have been deleted.")