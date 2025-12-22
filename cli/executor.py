"""Tool execution for Terminal AI Workflow CLI."""

import subprocess
import shutil
import time
from datetime import datetime
from pathlib import Path
from typing import Generator, Optional, Callable
from dataclasses import dataclass

from .config import get_config
from .router import Route


@dataclass
class ExecutionResult:
    """Result of tool execution."""
    tool: str
    task: str
    output: str
    exit_code: int
    duration: float
    output_file: Optional[Path] = None


def create_workspace() -> Path:
    """Create a timestamped workspace directory."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    workspace = Path("workspace") / timestamp
    workspace.mkdir(parents=True, exist_ok=True)
    return workspace


def check_tool_available(command: str) -> bool:
    """Check if a tool command is available in PATH."""
    return shutil.which(command) is not None


def get_tools_status() -> dict:
    """Get status of all configured tools."""
    config = get_config()
    status = {}

    for tool_name, tool_config in config.tools.items():
        command = tool_config.command
        available = check_tool_available(command) and config.is_tool_available(tool_name)
        status[tool_name] = {
            "name": tool_config.name,
            "command": command,
            "available": available
        }

    return status


def execute_tool_streaming(
    route: Route,
    workspace: Path,
    on_output: Callable[[str], None]
) -> ExecutionResult:
    """Execute a tool with streaming output.

    Args:
        route: The route containing tool and task info
        workspace: Directory to save output files
        on_output: Callback function called for each output chunk

    Returns:
        ExecutionResult with final output and status
    """
    config = get_config()
    command = config.get_tool_command(route.tool)

    output_file = workspace / f"{route.tool}_output.txt"
    buffer = ""
    start_time = time.time()
    exit_code = 0

    try:
        process = subprocess.Popen(
            [command, route.task],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            encoding='utf-8',
            errors='replace'
        )

        # Stream output line by line
        for line in iter(process.stdout.readline, ''):
            if not line:
                break
            buffer += line
            on_output(line)

        # Wait for completion
        process.wait()
        exit_code = process.returncode

    except FileNotFoundError:
        error_msg = f"Command not found: {command}\n"
        buffer = error_msg
        on_output(error_msg)
        exit_code = 1
    except Exception as e:
        error_msg = f"Error executing {command}: {str(e)}\n"
        buffer = error_msg
        on_output(error_msg)
        exit_code = 1

    duration = time.time() - start_time

    # Save output to file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(buffer)
    except Exception:
        pass

    return ExecutionResult(
        tool=route.tool,
        task=route.task,
        output=buffer,
        exit_code=exit_code,
        duration=duration,
        output_file=output_file
    )


def execute_tool_sync(route: Route, workspace: Path) -> ExecutionResult:
    """Execute a tool synchronously (non-streaming)."""
    config = get_config()
    command = config.get_tool_command(route.tool)

    output_file = workspace / f"{route.tool}_output.txt"
    start_time = time.time()

    try:
        result = subprocess.run(
            [command, route.task],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        output = result.stdout + result.stderr
        exit_code = result.returncode
    except subprocess.TimeoutExpired:
        output = "Error: Command timed out after 5 minutes"
        exit_code = 1
    except FileNotFoundError:
        output = f"Error: Command not found: {command}"
        exit_code = 1
    except Exception as e:
        output = f"Error: {str(e)}"
        exit_code = 1

    duration = time.time() - start_time

    # Save output to file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(output)
    except Exception:
        pass

    return ExecutionResult(
        tool=route.tool,
        task=route.task,
        output=output,
        exit_code=exit_code,
        duration=duration,
        output_file=output_file
    )
