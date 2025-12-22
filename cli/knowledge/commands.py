"""CLI command reference parser for Document Library."""

import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Optional

# Path to the command reference document
COMMAND_REF_PATH = Path("docs/library/AI_CLI_Commands_Reference.md")


@dataclass
class Command:
    """A single CLI command."""
    command: str
    description: str
    tool: str  # 'claude', 'gemini', 'openai'


@dataclass
class ToolOverview:
    """Overview of a CLI tool."""
    name: str
    tool_id: str
    description: str
    commands: List[Command]


# Cache for parsed commands
_commands_cache: Optional[Dict[str, List[Command]]] = None


def _parse_command_reference() -> Dict[str, List[Command]]:
    """Parse the AI_CLI_Commands_Reference.md file."""
    global _commands_cache
    if _commands_cache is not None:
        return _commands_cache

    result: Dict[str, List[Command]] = {
        "gemini": [],
        "openai": [],
        "claude": []
    }

    if not COMMAND_REF_PATH.exists():
        return result

    try:
        content = COMMAND_REF_PATH.read_text(encoding="utf-8")
    except Exception:
        return result

    # Split by major sections (## headers)
    sections = re.split(r'\n## \d+\. ', content)

    current_tool = None

    for section in sections:
        section = section.strip()
        if not section:
            continue

        # Determine which tool this section is about
        section_lower = section.lower()
        if "gemini" in section_lower[:100]:
            current_tool = "gemini"
        elif "openai" in section_lower[:100] or "codex" in section_lower[:100]:
            current_tool = "openai"
        elif "claude" in section_lower[:100]:
            current_tool = "claude"
        else:
            continue

        # Parse command entries
        commands = _parse_section_commands(section, current_tool)
        result[current_tool].extend(commands)

    _commands_cache = result
    return result


def _parse_section_commands(section: str, tool: str) -> List[Command]:
    """Parse commands from a section."""
    commands = []

    # Pattern for command entries: - `command` description
    # or: - `command` or `alias` description
    pattern = r'[-*]\s+`([^`]+)`(?:\s+or\s+`([^`]+)`)?\s+(.+?)(?=\n[-*]|\n###|\n##|\Z)'

    for match in re.finditer(pattern, section, re.DOTALL):
        cmd = match.group(1).strip()
        alias = match.group(2)
        desc = match.group(3).strip()

        # Clean up description
        desc = " ".join(desc.split())  # Normalize whitespace
        desc = desc[:200] if len(desc) > 200 else desc  # Truncate long descriptions

        commands.append(Command(command=cmd, description=desc, tool=tool))

        # Add alias as separate entry if exists
        if alias:
            commands.append(Command(command=alias.strip(), description=desc, tool=tool))

    # Also capture ### subsection commands (e.g., "### Flags")
    # Pattern: - `--flag` description
    flag_pattern = r'[-*]\s+`(--[a-z-]+(?:\s+<[^>]+>)?)`[,]?\s*`?-?[a-z]?`?\s*(.+?)(?=\n[-*]|\n###|\n##|\Z)'

    for match in re.finditer(flag_pattern, section, re.DOTALL):
        cmd = match.group(1).strip()
        desc = match.group(2).strip()
        desc = " ".join(desc.split())
        desc = desc[:200] if len(desc) > 200 else desc

        commands.append(Command(command=cmd, description=desc, tool=tool))

    return commands


def get_commands(tool: str) -> List[Command]:
    """Get all commands for a specific tool.

    Args:
        tool: One of 'claude', 'gemini', 'openai'

    Returns:
        List of Command objects
    """
    all_commands = _parse_command_reference()
    tool_lower = tool.lower()

    # Handle aliases
    if tool_lower in ("codex", "openai", "gpt"):
        tool_lower = "openai"
    elif tool_lower in ("anthropic",):
        tool_lower = "claude"
    elif tool_lower in ("google",):
        tool_lower = "gemini"

    return all_commands.get(tool_lower, [])


def search_commands(query: str) -> List[Command]:
    """Search for commands across all tools.

    Args:
        query: Search string

    Returns:
        List of matching Command objects
    """
    all_commands = _parse_command_reference()
    query_lower = query.lower()
    results = []

    for tool, commands in all_commands.items():
        for cmd in commands:
            if query_lower in cmd.command.lower() or query_lower in cmd.description.lower():
                results.append(cmd)

    return results


def get_all_tools_overview() -> List[ToolOverview]:
    """Get overview of all three CLI tools."""
    all_commands = _parse_command_reference()

    overviews = [
        ToolOverview(
            name="Gemini CLI",
            tool_id="gemini",
            description="Google's AI assistant - Research, exploration, web search",
            commands=all_commands.get("gemini", [])
        ),
        ToolOverview(
            name="Claude Code",
            tool_id="claude",
            description="Anthropic's AI assistant - Deep work, agents, complex tasks",
            commands=all_commands.get("claude", [])
        ),
        ToolOverview(
            name="OpenAI Codex",
            tool_id="openai",
            description="OpenAI's AI assistant - Analysis, code review, reasoning",
            commands=all_commands.get("openai", [])
        ),
    ]

    return overviews


def get_tool_quick_reference(tool: str) -> str:
    """Get a quick reference string for a tool's most common commands."""
    commands = get_commands(tool)

    if not commands:
        return f"No commands found for {tool}"

    # Take first 10 most important commands
    important = commands[:10]

    lines = [f"**{tool.title()} CLI Quick Reference**\n"]
    for cmd in important:
        lines.append(f"- `{cmd.command}` - {cmd.description[:80]}")

    return "\n".join(lines)
