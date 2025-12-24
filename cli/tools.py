"""Tool availability and execution management for Terminal AI Workflow CLI."""

import shutil
import subprocess
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from .config import get_config
from .errors import ToolNotFoundError, ToolNotAvailableError, ToolExecutionError


@dataclass
class ToolStatus:
    """Status information for a CLI tool."""
    name: str
    tool_id: str
    command: str
    installed: bool
    authenticated: bool
    available: bool  # installed AND authenticated
    version: Optional[str] = None
    error: Optional[str] = None


def check_tool_installed(command: str) -> Tuple[bool, Optional[str]]:
    """Check if a tool is installed on the system.

    Args:
        command: The command to check (e.g., 'claude', 'gemini')

    Returns:
        Tuple of (is_installed, version_or_error)
    """
    # First check if command exists in PATH
    if shutil.which(command) is None:
        return False, f"Command '{command}' not found in PATH"

    # Try to get version info
    try:
        result = subprocess.run(
            [command, "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            version = result.stdout.strip().split('\n')[0]
            return True, version
        else:
            # Command exists but --version failed, still consider installed
            return True, None
    except subprocess.TimeoutExpired:
        return True, "timeout checking version"
    except FileNotFoundError:
        return False, f"Command '{command}' not found"
    except Exception as e:
        # Command might exist but errored
        return True, str(e)


def get_tool_status(tool_id: str) -> ToolStatus:
    """Get comprehensive status for a specific tool.

    Args:
        tool_id: Tool identifier ('claude', 'gemini', 'openai')

    Returns:
        ToolStatus with all availability information
    """
    config = get_config()

    # Get tool config
    tool_config = config.tools.get(tool_id)
    if tool_config is None:
        return ToolStatus(
            name=tool_id.title(),
            tool_id=tool_id,
            command=tool_id,
            installed=False,
            authenticated=False,
            available=False,
            error=f"Tool '{tool_id}' not defined in configuration"
        )

    command = tool_config.command
    name = tool_config.name

    # Check if installed
    installed, version_or_error = check_tool_installed(command)

    # Check auth status from config/env
    auth_status = config.get_effective_auth_status(tool_id)
    authenticated = auth_status is True

    # Available = installed AND not explicitly unauthenticated
    available = installed and (auth_status is not False)

    return ToolStatus(
        name=name,
        tool_id=tool_id,
        command=command,
        installed=installed,
        authenticated=authenticated,
        available=available,
        version=version_or_error if installed else None,
        error=version_or_error if not installed else None
    )


def get_all_tools_status() -> List[ToolStatus]:
    """Get status for all configured tools.

    Returns:
        List of ToolStatus for each tool
    """
    config = get_config()
    return [get_tool_status(tool_id) for tool_id in config.tools.keys()]


def require_tool(tool_id: str) -> ToolStatus:
    """Require a tool to be available, raising an error if not.

    Args:
        tool_id: Tool identifier

    Returns:
        ToolStatus if available

    Raises:
        ToolNotFoundError: If tool is not installed
        ToolNotAvailableError: If tool is installed but not authenticated
    """
    status = get_tool_status(tool_id)

    if not status.installed:
        raise ToolNotFoundError(tool_id, status.command)

    if not status.authenticated:
        raise ToolNotAvailableError(tool_id, "not authenticated in config")

    return status


def get_available_tools() -> List[str]:
    """Get list of tool IDs that are currently available.

    Returns:
        List of available tool IDs
    """
    statuses = get_all_tools_status()
    return [s.tool_id for s in statuses if s.available]


def get_best_available_tool(preferred: List[str]) -> Optional[str]:
    """Get the first available tool from a preference list.

    Args:
        preferred: List of tool IDs in order of preference

    Returns:
        First available tool ID, or None if none available
    """
    available = set(get_available_tools())
    for tool_id in preferred:
        if tool_id in available:
            return tool_id
    return None


def execute_tool(tool_id: str, args: List[str], timeout: int = 300) -> Tuple[int, str, str]:
    """Execute a tool command.

    Args:
        tool_id: Tool identifier
        args: Command arguments
        timeout: Timeout in seconds

    Returns:
        Tuple of (exit_code, stdout, stderr)

    Raises:
        ToolNotFoundError: If tool not installed
        ToolNotAvailableError: If tool not authenticated
        ToolExecutionError: If execution fails
    """
    status = require_tool(tool_id)

    try:
        result = subprocess.run(
            [status.command] + args,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        raise ToolExecutionError(
            tool_id, status.command, -1,
            f"Command timed out after {timeout} seconds"
        )
    except FileNotFoundError:
        raise ToolNotFoundError(tool_id, status.command)
    except Exception as e:
        raise ToolExecutionError(tool_id, status.command, -1, str(e))


def format_tools_status_table(statuses: List[ToolStatus]) -> str:
    """Format tool statuses as a text table.

    Args:
        statuses: List of ToolStatus objects

    Returns:
        Formatted table string
    """
    lines = ["Tool Status:", ""]
    lines.append(f"{'Tool':<15} {'Command':<10} {'Installed':<10} {'Auth':<10} {'Status':<10}")
    lines.append("-" * 55)

    for s in statuses:
        installed = "Yes" if s.installed else "No"
        auth = "Yes" if s.authenticated else "No"
        status = "Ready" if s.available else "Unavailable"

        lines.append(f"{s.name:<15} {s.command:<10} {installed:<10} {auth:<10} {status:<10}")

        if s.error:
            lines.append(f"  Error: {s.error}")
        elif s.version:
            lines.append(f"  Version: {s.version}")

    return "\n".join(lines)
