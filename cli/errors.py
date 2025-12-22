"""Custom exceptions and error handling for Terminal AI Workflow CLI."""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any


class CLIError(Exception):
    """Base exception for CLI errors."""

    def __init__(self, message: str, hint: Optional[str] = None):
        self.message = message
        self.hint = hint
        super().__init__(message)

    def __str__(self) -> str:
        if self.hint:
            return f"{self.message}\n  Hint: {self.hint}"
        return self.message


class ConfigError(CLIError):
    """Configuration-related errors."""
    pass


class ConfigNotFoundError(ConfigError):
    """Configuration file not found."""

    def __init__(self, path: str):
        super().__init__(
            f"Configuration file not found: {path}",
            hint="Run 'python -m cli init' to create a default configuration"
        )
        self.path = path


class ConfigValidationError(ConfigError):
    """Configuration validation failed."""

    def __init__(self, errors: List[str]):
        self.errors = errors
        message = "Configuration validation failed:\n" + "\n".join(f"  - {e}" for e in errors)
        super().__init__(message, hint="Check config/role_config.json for issues")


class ConfigParseError(ConfigError):
    """Configuration file parsing failed."""

    def __init__(self, path: str, detail: str):
        super().__init__(
            f"Failed to parse configuration file: {path}\n  {detail}",
            hint="Ensure the file contains valid JSON"
        )
        self.path = path
        self.detail = detail


class ToolError(CLIError):
    """Tool-related errors."""
    pass


class ToolNotFoundError(ToolError):
    """CLI tool not found on system."""

    def __init__(self, tool: str, command: str):
        self.tool = tool
        self.command = command
        super().__init__(
            f"Tool '{tool}' not found (command: {command})",
            hint=f"Install {tool} or check that '{command}' is in your PATH"
        )


class ToolNotAvailableError(ToolError):
    """Tool exists but is not authenticated/configured."""

    def __init__(self, tool: str, reason: str = "not authenticated"):
        self.tool = tool
        self.reason = reason
        super().__init__(
            f"Tool '{tool}' is not available: {reason}",
            hint=f"Run '{tool} auth' or update auth_status in config"
        )


class ToolExecutionError(ToolError):
    """Tool command execution failed."""

    def __init__(self, tool: str, command: str, exit_code: int, stderr: str = ""):
        self.tool = tool
        self.command = command
        self.exit_code = exit_code
        self.stderr = stderr
        message = f"Tool '{tool}' failed with exit code {exit_code}"
        if stderr:
            message += f"\n  Error: {stderr[:200]}"
        super().__init__(message)


class RoutingError(CLIError):
    """Routing-related errors."""
    pass


class NoAvailableToolError(RoutingError):
    """No tools available for routing."""

    def __init__(self):
        super().__init__(
            "No AI tools are available for routing",
            hint="Check auth_status in config or install at least one tool (claude, gemini, codex)"
        )


class KnowledgeError(CLIError):
    """Knowledge module errors."""
    pass


class DocumentNotFoundError(KnowledgeError):
    """Document not found in library."""

    def __init__(self, name: str):
        self.name = name
        super().__init__(
            f"Document not found: {name}",
            hint="Use '/docs' to list available documents"
        )


class IndexError(KnowledgeError):
    """Document index error."""

    def __init__(self, detail: str):
        super().__init__(
            f"Document index error: {detail}",
            hint="Try '/docs refresh' to rebuild the index"
        )


@dataclass
class ValidationResult:
    """Result of configuration validation."""
    valid: bool
    errors: List[str]
    warnings: List[str]

    @classmethod
    def success(cls) -> "ValidationResult":
        return cls(valid=True, errors=[], warnings=[])

    @classmethod
    def failure(cls, errors: List[str], warnings: List[str] = None) -> "ValidationResult":
        return cls(valid=False, errors=errors, warnings=warnings or [])


def validate_config_data(data: Dict[str, Any]) -> ValidationResult:
    """Validate configuration data structure.

    Args:
        data: Parsed JSON configuration data

    Returns:
        ValidationResult with errors and warnings
    """
    errors = []
    warnings = []

    # Check required top-level keys
    required_keys = ["roles", "tools", "auth_status"]
    for key in required_keys:
        if key not in data:
            errors.append(f"Missing required key: '{key}'")

    if errors:
        # Can't continue validation without required keys
        return ValidationResult.failure(errors)

    # Validate roles
    roles = data.get("roles", {})
    if not roles:
        warnings.append("No roles defined - routing will use defaults")
    else:
        for role_name, role_data in roles.items():
            if not isinstance(role_data, dict):
                errors.append(f"Role '{role_name}' must be an object")
                continue

            if "keywords" not in role_data:
                errors.append(f"Role '{role_name}' missing 'keywords' array")
            elif not isinstance(role_data["keywords"], list):
                errors.append(f"Role '{role_name}' keywords must be an array")
            elif not role_data["keywords"]:
                warnings.append(f"Role '{role_name}' has no keywords defined")

            if "primary" not in role_data:
                errors.append(f"Role '{role_name}' missing 'primary' tool")

    # Validate tools
    tools = data.get("tools", {})
    if not tools:
        errors.append("No tools defined - at least one tool is required")
    else:
        for tool_name, tool_data in tools.items():
            if not isinstance(tool_data, dict):
                errors.append(f"Tool '{tool_name}' must be an object")
                continue

            if "command" not in tool_data:
                warnings.append(f"Tool '{tool_name}' missing 'command' - will use tool name")

    # Validate auth_status
    auth_status = data.get("auth_status", {})
    if not auth_status:
        warnings.append("No auth_status defined - all tools will be marked unavailable")

    # Cross-reference validation
    for role_name, role_data in roles.items():
        if isinstance(role_data, dict):
            primary = role_data.get("primary")
            if primary and primary not in tools:
                errors.append(f"Role '{role_name}' references unknown tool: '{primary}'")

            for fallback in role_data.get("fallback", []):
                if fallback not in tools:
                    warnings.append(f"Role '{role_name}' fallback references unknown tool: '{fallback}'")

    # Check for tools without auth_status
    for tool_name in tools:
        if tool_name not in auth_status:
            warnings.append(f"Tool '{tool_name}' has no auth_status entry")

    if errors:
        return ValidationResult.failure(errors, warnings)

    return ValidationResult(valid=True, errors=[], warnings=warnings)


def format_error_for_display(error: CLIError) -> str:
    """Format an error for rich console display.

    Args:
        error: The CLIError to format

    Returns:
        Formatted string for display
    """
    lines = [f"[red]Error:[/red] {error.message}"]
    if error.hint:
        lines.append(f"[dim]Hint: {error.hint}[/dim]")
    return "\n".join(lines)
