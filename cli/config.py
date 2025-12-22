"""Configuration management for Terminal AI Workflow CLI."""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from dotenv import load_dotenv


@dataclass
class ToolConfig:
    """Configuration for a single AI tool."""
    name: str
    command: str
    context_file: str


@dataclass
class RoleConfig:
    """Configuration for a routing role."""
    keywords: List[str]
    primary: str
    fallback: List[str] = field(default_factory=list)


@dataclass
class Config:
    """Main configuration container."""
    roles: Dict[str, RoleConfig]
    tools: Dict[str, ToolConfig]
    auth_status: Dict[str, bool]

    @classmethod
    def load(cls, config_path: Optional[Path] = None) -> "Config":
        """Load configuration from role_config.json and .env files."""
        # Load .env file
        load_dotenv()

        # Determine config path
        if config_path is None:
            config_path = Path("config/role_config.json")

        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")

        with open(config_path, "r") as f:
            data = json.load(f)

        # Parse roles
        roles = {}
        for role_name, role_data in data.get("roles", {}).items():
            roles[role_name] = RoleConfig(
                keywords=role_data.get("keywords", []),
                primary=role_data.get("primary", "claude"),
                fallback=role_data.get("fallback", [])
            )

        # Parse tools
        tools = {}
        for tool_name, tool_data in data.get("tools", {}).items():
            tools[tool_name] = ToolConfig(
                name=tool_data.get("name", tool_name),
                command=tool_data.get("command", tool_name),
                context_file=tool_data.get("context_file", f"{tool_name.upper()}.md")
            )

        # Parse auth status
        auth_status = data.get("auth_status", {})

        return cls(roles=roles, tools=tools, auth_status=auth_status)

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
