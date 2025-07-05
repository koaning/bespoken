"""Command execution tools for the bespoken assistant."""

from typing import Optional
from pathlib import Path
import subprocess
import shutil
import llm

from .. import config
from .. import ui


def run_command(command: str, working_directory: Optional[str] = ".", timeout: int = 30) -> str:
    """Execute any shell command and return the output. Full access to the system."""
    config.tool_debug(f">>> LLM calling tool: run_command(command={repr(command)}, working_directory={repr(working_directory)}, timeout={timeout})")
    config.tool_status(f"Preparing to execute command: {command}")
    
    # Ask for confirmation before executing
    ui.print(f"[bold]Command to execute:[/bold] {command}")
    if working_directory != ".":
        ui.print(f"[bold]Working directory:[/bold] {working_directory}")
    ui.print(f"[bold]Timeout:[/bold] {timeout} seconds")
    
    confirm = ui.confirm("Execute this command?", default=True)
    if not confirm:
        config.tool_error("Command execution cancelled by user.")
        return "IMPORTANT: The user declined to execute the command. Do not continue with this task. Wait for new instructions from the user."
    
    # Resolve working directory
    if working_directory:
        work_dir = Path(working_directory).resolve()
        if not work_dir.is_dir():
            return f"Error: Working directory '{working_directory}' does not exist or is not a directory"
    else:
        work_dir = Path(".").resolve()
    
    config.tool_status(f"Executing command: {command}")
    
    try:
        # Execute the command
        result = subprocess.run(
            command,
            shell=True,
            cwd=work_dir,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        # Format the output
        output_lines = []
        if result.stdout:
            output_lines.append("STDOUT:")
            output_lines.append(result.stdout.rstrip())
        
        if result.stderr:
            output_lines.append("STDERR:")
            output_lines.append(result.stderr.rstrip())
        
        output_lines.append(f"Exit code: {result.returncode}")
        
        output = "\n".join(output_lines)
        
        if result.returncode != 0:
            config.tool_warning(f"Command failed with exit code {result.returncode}")
        else:
            config.tool_success(f"Command executed successfully")
        
        return output
        
    except subprocess.TimeoutExpired:
        return f"Error: Command timed out after {timeout} seconds"
    except Exception as e:
        return f"Error executing command: {e}"


class GitTool(llm.Toolbox):
    """Git command execution tool - safe git operations only."""
    
    def __init__(self, auto_trust: bool = False):
        self.tool_name = "GitTool"
        if auto_trust:
            ui.trust_tool(self.tool_name)
    
    def _run_git(self, git_args: str, working_directory: Optional[str] = None) -> str:
        """Internal method to run git commands."""
        command = f"git {git_args}"
        
        # Ask for confirmation unless trusted
        if not ui.confirm_tool_action(
            self.tool_name, 
            f"Execute: {command}",
            {"Working directory": working_directory} if working_directory else None
        ):
            config.tool_error("Git command cancelled by user.")
            return "IMPORTANT: The user declined the git command. Do not continue with this task."
        
        config.tool_status(f"Executing: {command}")
        
        # Execute without the general run_command confirmation
        work_dir = Path(working_directory).resolve() if working_directory else Path(".").resolve()
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=work_dir,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            output = result.stdout + result.stderr
            if result.returncode != 0:
                config.tool_warning(f"Git command failed with exit code {result.returncode}")
            
            return output.strip()
            
        except Exception as e:
            return f"Error executing git command: {e}"
    
    def status(self, working_directory: Optional[str] = None) -> str:
        """Get git status."""
        config.tool_debug(f">>> LLM calling tool: GitTool.status(working_directory={repr(working_directory)})")
        return self._run_git("status", working_directory)
    
    def log(self, args: str = "--oneline -10", working_directory: Optional[str] = None) -> str:
        """Get git log. Default: last 10 commits in oneline format."""
        config.tool_debug(f">>> LLM calling tool: GitTool.log(args={repr(args)}, working_directory={repr(working_directory)})")
        return self._run_git(f"log {args}", working_directory)
    
    def diff(self, args: str = "", working_directory: Optional[str] = None) -> str:
        """Get git diff."""
        config.tool_debug(f">>> LLM calling tool: GitTool.diff(args={repr(args)}, working_directory={repr(working_directory)})")
        return self._run_git(f"diff {args}", working_directory)
    
    def branch(self, args: str = "-a", working_directory: Optional[str] = None) -> str:
        """List git branches. Default: all branches."""
        config.tool_debug(f">>> LLM calling tool: GitTool.branch(args={repr(args)}, working_directory={repr(working_directory)})")
        return self._run_git(f"branch {args}", working_directory)


class NpmTool(llm.Toolbox):
    """NPM command execution tool - safe npm operations only."""
    
    def __init__(self, auto_trust: bool = False):
        self.tool_name = "NpmTool"
        if auto_trust:
            ui.trust_tool(self.tool_name)
    
    def _run_npm(self, npm_args: str, working_directory: Optional[str] = None) -> str:
        """Internal method to run npm commands."""
        command = f"npm {npm_args}"
        
        # Ask for confirmation unless trusted
        if not ui.confirm_tool_action(
            self.tool_name, 
            f"Execute: {command}",
            {"Working directory": working_directory} if working_directory else None
        ):
            config.tool_error("NPM command cancelled by user.")
            return "IMPORTANT: The user declined the npm command. Do not continue with this task."
        
        config.tool_status(f"Executing: {command}")
        
        work_dir = Path(working_directory).resolve() if working_directory else Path(".").resolve()
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=work_dir,
                capture_output=True,
                text=True,
                timeout=60  # NPM commands can take longer
            )
            
            output = result.stdout + result.stderr
            if result.returncode != 0:
                config.tool_warning(f"NPM command failed with exit code {result.returncode}")
            
            return output.strip()
            
        except Exception as e:
            return f"Error executing npm command: {e}"
    
    def list(self, depth: int = 0, working_directory: Optional[str] = None) -> str:
        """List installed packages."""
        config.tool_debug(f">>> LLM calling tool: NpmTool.list(depth={depth}, working_directory={repr(working_directory)})")
        args = f"list --depth={depth}"
        return self._run_npm(args, working_directory)
    
    def outdated(self, working_directory: Optional[str] = None) -> str:
        """Check for outdated packages."""
        config.tool_debug(f">>> LLM calling tool: NpmTool.outdated(working_directory={repr(working_directory)})")
        return self._run_npm("outdated", working_directory)
    
    def audit(self, fix: bool = False, working_directory: Optional[str] = None) -> str:
        """Run security audit. Set fix=True to auto-fix issues."""
        config.tool_debug(f">>> LLM calling tool: NpmTool.audit(fix={fix}, working_directory={repr(working_directory)})")
        args = "audit fix" if fix else "audit"
        return self._run_npm(args, working_directory)
    
    def scripts(self, working_directory: Optional[str] = None) -> str:
        """List available npm scripts from package.json."""
        config.tool_debug(f">>> LLM calling tool: NpmTool.scripts(working_directory={repr(working_directory)})")
        return self._run_npm("run", working_directory)


class PythonTool(llm.Toolbox):
    """Python command execution tool - safe python operations only."""
    
    def __init__(self, auto_trust: bool = False, uv: bool = True):
        self.tool_name = "PythonTool"
        self.use_uv = uv
        if auto_trust:
            ui.trust_tool(self.tool_name)
    
    def _run_python(self, python_args: str, working_directory: Optional[str] = None) -> str:
        """Internal method to run python commands."""
        command = f"python {python_args}"
        
        # Ask for confirmation unless trusted
        if not ui.confirm_tool_action(
            self.tool_name, 
            f"Execute: {command}",
            {"Working directory": working_directory} if working_directory else None
        ):
            config.tool_error("Python command cancelled by user.")
            return "IMPORTANT: The user declined the python command. Do not continue with this task."
        
        config.tool_status(f"Executing: {command}")
        
        work_dir = Path(working_directory).resolve() if working_directory else Path(".").resolve()
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=work_dir,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            output = result.stdout + result.stderr
            if result.returncode != 0:
                config.tool_warning(f"Python command failed with exit code {result.returncode}")
            
            return output.strip()
            
        except Exception as e:
            return f"Error executing python command: {e}"
    
    def _run_uv_command(self, command: str, working_directory: Optional[str] = None) -> str:
        """Internal method to run uv commands."""
        # Ask for confirmation unless trusted
        if not ui.confirm_tool_action(
            self.tool_name, 
            f"Execute: {command}",
            {"Working directory": working_directory} if working_directory else None
        ):
            config.tool_error("UV command cancelled by user.")
            return "IMPORTANT: The user declined the uv command. Do not continue with this task."
        
        config.tool_status(f"Executing: {command}")
        
        work_dir = Path(working_directory).resolve() if working_directory else Path(".").resolve()
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=work_dir,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            output = result.stdout + result.stderr
            if result.returncode != 0:
                config.tool_warning(f"UV command failed with exit code {result.returncode}")
            
            return output.strip()
            
        except Exception as e:
            return f"Error executing uv command: {e}"
    
    def version(self) -> str:
        """Get Python version."""
        config.tool_debug(">>> LLM calling tool: PythonTool.version()")
        return self._run_python("--version")
    
    def pip_list(self, format: str = "columns", working_directory: Optional[str] = None) -> str:
        """List installed packages. Format can be: columns, freeze, json."""
        config.tool_debug(f">>> LLM calling tool: PythonTool.pip_list(format={repr(format)}, working_directory={repr(working_directory)})")
        if self.use_uv:
            # Use uv pip instead of python -m pip
            command = f"uv pip list --format={format}"
            return self._run_uv_command(command, working_directory)
        else:
            args = f"-m pip list --format={format}"
            return self._run_python(args, working_directory)
    
    def pip_show(self, package: str, working_directory: Optional[str] = None) -> str:
        """Show details about a specific package."""
        config.tool_debug(f">>> LLM calling tool: PythonTool.pip_show(package={repr(package)}, working_directory={repr(working_directory)})")
        if self.use_uv:
            command = f"uv pip show {package}"
            return self._run_uv_command(command, working_directory)
        else:
            return self._run_python(f"-m pip show {package}", working_directory)
    
    def check_import(self, module: str, working_directory: Optional[str] = None) -> str:
        """Check if a module can be imported."""
        config.tool_debug(f">>> LLM calling tool: PythonTool.check_import(module={repr(module)}, working_directory={repr(working_directory)})")
        code = f"-c \"import {module}; print('{module} imported successfully')\""
        return self._run_python(code, working_directory)