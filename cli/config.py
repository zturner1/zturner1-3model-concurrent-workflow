"""Configuration management for Terminal AI Workflow CLI."""

import json
import os
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from dotenv import load_dotenv

from .errors import (
    ConfigNotFoundError, ConfigParseError, ConfigValidationError,
    validate_config_data, ValidationResult
)


@dataclass
class ToolConfig:
    """Configuration for a single AI tool."""
    name: str
    command: str
    context_file: str
    role: str = ""
    args: List[str] = field(default_factory=list)


@dataclass
class RoleConfig:
    """Configuration for a routing role."""
    keywords: List[str]
    primary: str
    fallback: List[str] = field(default_factory=list)
    description: str = ""


@dataclass
class Config:
    """Main configuration container."""
    roles: Dict[str, RoleConfig]
    tools: Dict[str, ToolConfig]
    auth_status: Dict[str, object]
    _warnings: List[str] = field(default_factory=list)

    @classmethod
    def load(cls, config_path: Optional[Path] = None, validate: bool = True) -> "Config":
        """Load configuration from role_config.json and .env files.

        Args:
            config_path: Path to config file (defaults to config/role_config.json)
            validate: Whether to validate the config (default True)

        Returns:
            Config instance

        Raises:
            ConfigNotFoundError: If config file doesn't exist
            ConfigParseError: If config file contains invalid JSON
            ConfigValidationError: If validation fails
        """
        # Load .env file
        load_dotenv()

        # Determine config path
        if config_path is None:
            config_path = Path("config/role_config.json")

        if not config_path.exists():
            raise ConfigNotFoundError(str(config_path))

        try:
            with open(config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise ConfigParseError(str(config_path), str(e))

        # Validate configuration
        warnings = []
        if validate:
            result = validate_config_data(data)
            if not result.valid:
                raise ConfigValidationError(result.errors)
            warnings = result.warnings

        # Parse roles
        roles = {}
        for role_name, role_data in data.get("roles", {}).items():
            roles[role_name] = RoleConfig(
                keywords=role_data.get("keywords", []),
                primary=role_data.get("primary", "claude"),
                fallback=role_data.get("fallback", []),
                description=role_data.get("description", "")
            )

        # Parse tools
        default_args = {
            "claude": ["-p"],
            "gemini": ["-p"],
        }
        tools = {}
        for tool_name, tool_data in data.get("tools", {}).items():
            tool_args = tool_data.get("args")
            if not isinstance(tool_args, list):
                tool_args = default_args.get(tool_name, [])

            tools[tool_name] = ToolConfig(
                name=tool_data.get("name", tool_name),
                command=tool_data.get("command", tool_name),
                context_file=tool_data.get("context_file", f"{tool_name.upper()}.md"),
                role=tool_data.get("role", ""),
                args=tool_args
            )

        # Parse auth status
        auth_status = data.get("auth_status", {})

        config = cls(roles=roles, tools=tools, auth_status=auth_status)
        config._warnings = warnings
        return config

    @property
    def warnings(self) -> List[str]:
        """Get any warnings from config loading."""
        return self._warnings

    def get_auth_status(self, tool: str) -> Optional[bool]:
        """Get configured auth status.

        Returns True/False if explicitly set, None if auto/unknown.
        """
        status = self.auth_status.get(tool, "auto")
        if isinstance(status, bool):
            return status
        if isinstance(status, str):
            lowered = status.strip().lower()
            if lowered in ("true", "false"):
                return lowered == "true"
            if lowered == "auto":
                return None
        return None

    def _detect_auth_status(self, tool: str) -> Optional[bool]:
        """Best-effort auth detection from environment."""
        if tool == "openai":
            return True if os.environ.get("OPENAI_API_KEY") else None
        if tool == "claude":
            return True if os.environ.get("ANTHROPIC_API_KEY") else None
        if tool == "gemini":
            return True if (os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")) else None
        return None

    def get_effective_auth_status(self, tool: str) -> Optional[bool]:
        """Resolve auth status using config + best-effort detection."""
        status = self.get_auth_status(tool)
        if status is not None:
            return status
        return self._detect_auth_status(tool)

    def is_tool_installed(self, tool: str) -> bool:
        """Check if a tool's command is available on PATH."""
        if tool not in self.tools:
            return False
        command = self.get_tool_command(tool)
        return shutil.which(command) is not None

    def is_tool_available(self, tool: str) -> bool:
        """Check if a tool is available based on auth + install state."""
        if tool not in self.tools:
            return False
        auth_status = self.get_auth_status(tool)
        if auth_status is True:
            return True
        if auth_status is False:
            return False

        if not self.is_tool_installed(tool):
            return False

        detected = self.get_effective_auth_status(tool)
        if detected is False:
            return False
        return True

    def get_tool_command(self, tool: str) -> str:
        """Get the command for a tool."""
        if tool in self.tools:
            return self.tools[tool].command
        # Fallback to tool name as command
        return tool


# Global config instance
_config: Optional[Config] = None


def get_config() -> Config:
    """Get or load the global config instance."""
    global _config
    if _config is None:
        _config = Config.load()
    return _config


def reload_config() -> Config:
    """Force reload of configuration."""
    global _config
    _config = Config.load()
    return _config


def _reset_config() -> None:
    """Reset the config singleton (for testing)."""
    global _config
    _config = None


def load_config(config_path: Path) -> Config:
    """Load configuration from a specific path."""
    return Config.load(config_path)
