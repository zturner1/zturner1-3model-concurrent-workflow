"""Configuration management for Terminal AI Workflow CLI."""

import json
import os
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
    auth_status: Dict[str, bool]
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
        tools = {}
        for tool_name, tool_data in data.get("tools", {}).items():
            tools[tool_name] = ToolConfig(
                name=tool_data.get("name", tool_name),
                command=tool_data.get("command", tool_name),
                context_file=tool_data.get("context_file", f"{tool_name.upper()}.md"),
                role=tool_data.get("role", "")
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

    def is_tool_available(self, tool: str) -> bool:
        """Check if a tool is available based on auth status."""
        return self.auth_status.get(tool, False)

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
