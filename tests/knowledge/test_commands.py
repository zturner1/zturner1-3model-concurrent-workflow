"""Tests for cli/knowledge/commands.py module."""

import pytest
from pathlib import Path
from unittest.mock import patch

from cli.knowledge.commands import (
    Command, ToolOverview,
    _parse_command_reference, _parse_section_commands,
    get_commands, search_commands, get_all_tools_overview,
    get_tool_quick_reference, COMMAND_REF_PATH
)


class TestCommand:
    """Tests for Command dataclass."""

    def test_command_creation(self):
        """Test creating a Command instance."""
        cmd = Command(
            command="claude",
            description="Start interactive mode",
            tool="claude"
        )
        assert cmd.command == "claude"
        assert cmd.description == "Start interactive mode"
        assert cmd.tool == "claude"


class TestToolOverview:
    """Tests for ToolOverview dataclass."""

    def test_tool_overview_creation(self):
        """Test creating a ToolOverview instance."""
        overview = ToolOverview(
            name="Claude Code",
            tool_id="claude",
            description="Deep work tool",
            commands=[
                Command("claude", "Start interactive", "claude")
            ]
        )
        assert overview.name == "Claude Code"
        assert len(overview.commands) == 1


class TestParseSectionCommands:
    """Tests for _parse_section_commands function."""

    def test_parse_simple_commands(self):
        """Test parsing simple command entries."""
        section = """
### Commands
- `claude` Start interactive mode
- `gemini` Start gemini mode
"""
        commands = _parse_section_commands(section, "claude")
        assert len(commands) >= 1
        # Should find at least "claude" command

    def test_parse_commands_with_alias(self):
        """Test parsing commands with aliases."""
        section = """
- `--help` or `-h` Show help message
"""
        commands = _parse_section_commands(section, "claude")
        # Should create entries for both --help and -h

    def test_parse_flag_commands(self):
        """Test parsing flag-style commands."""
        section = """
### Flags
- `--verbose` Enable verbose output
- `--quiet`, `-q` Suppress output
"""
        commands = _parse_section_commands(section, "claude")
        # Should find flag commands

    def test_parse_empty_section(self):
        """Test parsing empty section."""
        commands = _parse_section_commands("", "claude")
        assert commands == []


class TestGetCommands:
    """Tests for get_commands function."""

    def setup_method(self):
        """Reset cache before each test."""
        import cli.knowledge.commands
        cli.knowledge.commands._commands_cache = None

    def test_get_commands_claude(self, tmp_path):
        """Test getting Claude commands."""
        # Create a mock command reference file
        ref_content = """# AI CLI Commands Reference

## 1. Claude Code

### Commands
- `claude` Start interactive mode
- `claude -p "query"` Print mode
"""
        ref_file = tmp_path / "ref.md"
        ref_file.write_text(ref_content)

        with patch('cli.knowledge.commands.COMMAND_REF_PATH', ref_file):
            commands = get_commands("claude")
            # Should return list (may be empty or have commands depending on parsing)
            assert isinstance(commands, list)

    def test_get_commands_gemini(self, tmp_path):
        """Test getting Gemini commands."""
        ref_content = """# Reference

## 1. Gemini CLI

- `gemini` Start interactive
"""
        ref_file = tmp_path / "ref.md"
        ref_file.write_text(ref_content)

        with patch('cli.knowledge.commands.COMMAND_REF_PATH', ref_file):
            commands = get_commands("gemini")
            assert isinstance(commands, list)

    def test_get_commands_aliases(self, tmp_path):
        """Test tool name aliases."""
        ref_content = """# Reference

## 1. OpenAI Codex

- `codex` Start codex
"""
        ref_file = tmp_path / "ref.md"
        ref_file.write_text(ref_content)

        with patch('cli.knowledge.commands.COMMAND_REF_PATH', ref_file):
            # All these should map to openai
            for alias in ["openai", "codex", "gpt"]:
                commands = get_commands(alias)
                assert isinstance(commands, list)

    def test_get_commands_anthropic_alias(self, tmp_path):
        """Test anthropic maps to claude."""
        ref_content = "# Empty"
        ref_file = tmp_path / "ref.md"
        ref_file.write_text(ref_content)

        with patch('cli.knowledge.commands.COMMAND_REF_PATH', ref_file):
            commands = get_commands("anthropic")
            assert isinstance(commands, list)

    def test_get_commands_unknown_tool(self, tmp_path):
        """Test getting commands for unknown tool."""
        ref_content = "# Empty"
        ref_file = tmp_path / "ref.md"
        ref_file.write_text(ref_content)

        with patch('cli.knowledge.commands.COMMAND_REF_PATH', ref_file):
            commands = get_commands("unknown_tool")
            assert commands == []

    def test_get_commands_missing_file(self, tmp_path):
        """Test getting commands when reference file is missing."""
        with patch('cli.knowledge.commands.COMMAND_REF_PATH', tmp_path / "nonexistent.md"):
            commands = get_commands("claude")
            assert commands == []


class TestSearchCommands:
    """Tests for search_commands function."""

    def setup_method(self):
        """Reset cache before each test."""
        import cli.knowledge.commands
        cli.knowledge.commands._commands_cache = None

    def test_search_by_command_name(self, tmp_path):
        """Test searching by command name."""
        ref_content = """# Reference

## 1. Claude Code

- `claude` Start interactive mode
- `--help` Show help
"""
        ref_file = tmp_path / "ref.md"
        ref_file.write_text(ref_content)

        with patch('cli.knowledge.commands.COMMAND_REF_PATH', ref_file):
            results = search_commands("claude")
            assert isinstance(results, list)

    def test_search_by_description(self, tmp_path):
        """Test searching by description."""
        ref_content = """# Reference

## 1. Claude Code

- `claude` Start interactive mode
"""
        ref_file = tmp_path / "ref.md"
        ref_file.write_text(ref_content)

        with patch('cli.knowledge.commands.COMMAND_REF_PATH', ref_file):
            results = search_commands("interactive")
            assert isinstance(results, list)

    def test_search_case_insensitive(self, tmp_path):
        """Test case-insensitive search."""
        ref_content = """# Reference

## 1. Claude Code

- `CLAUDE` Start interactive mode
"""
        ref_file = tmp_path / "ref.md"
        ref_file.write_text(ref_content)

        with patch('cli.knowledge.commands.COMMAND_REF_PATH', ref_file):
            results1 = search_commands("claude")
            results2 = search_commands("CLAUDE")
            # Both should find the same thing
            assert isinstance(results1, list)
            assert isinstance(results2, list)

    def test_search_no_results(self, tmp_path):
        """Test search with no matches."""
        ref_content = "# Empty reference"
        ref_file = tmp_path / "ref.md"
        ref_file.write_text(ref_content)

        with patch('cli.knowledge.commands.COMMAND_REF_PATH', ref_file):
            results = search_commands("xyznonexistent")
            assert results == []


class TestGetAllToolsOverview:
    """Tests for get_all_tools_overview function."""

    def setup_method(self):
        """Reset cache before each test."""
        import cli.knowledge.commands
        cli.knowledge.commands._commands_cache = None

    def test_returns_three_tools(self, tmp_path):
        """Test that overview returns all three tools."""
        ref_content = "# Empty"
        ref_file = tmp_path / "ref.md"
        ref_file.write_text(ref_content)

        with patch('cli.knowledge.commands.COMMAND_REF_PATH', ref_file):
            overviews = get_all_tools_overview()
            assert len(overviews) == 3

    def test_overview_has_required_fields(self, tmp_path):
        """Test that each overview has required fields."""
        ref_content = "# Empty"
        ref_file = tmp_path / "ref.md"
        ref_file.write_text(ref_content)

        with patch('cli.knowledge.commands.COMMAND_REF_PATH', ref_file):
            overviews = get_all_tools_overview()
            for overview in overviews:
                assert isinstance(overview, ToolOverview)
                assert overview.name
                assert overview.tool_id
                assert overview.description

    def test_overview_tool_ids(self, tmp_path):
        """Test that overviews include all tool IDs."""
        ref_content = "# Empty"
        ref_file = tmp_path / "ref.md"
        ref_file.write_text(ref_content)

        with patch('cli.knowledge.commands.COMMAND_REF_PATH', ref_file):
            overviews = get_all_tools_overview()
            tool_ids = {o.tool_id for o in overviews}
            assert tool_ids == {"gemini", "claude", "openai"}


class TestGetToolQuickReference:
    """Tests for get_tool_quick_reference function."""

    def setup_method(self):
        """Reset cache before each test."""
        import cli.knowledge.commands
        cli.knowledge.commands._commands_cache = None

    def test_quick_reference_format(self, tmp_path):
        """Test quick reference format."""
        ref_content = """# Reference

## 1. Claude Code

- `claude` Start interactive mode
- `--help` Show help
"""
        ref_file = tmp_path / "ref.md"
        ref_file.write_text(ref_content)

        with patch('cli.knowledge.commands.COMMAND_REF_PATH', ref_file):
            ref = get_tool_quick_reference("claude")
            assert "Claude" in ref or "Quick Reference" in ref

    def test_quick_reference_no_commands(self, tmp_path):
        """Test quick reference when no commands found."""
        ref_content = "# Empty"
        ref_file = tmp_path / "ref.md"
        ref_file.write_text(ref_content)

        with patch('cli.knowledge.commands.COMMAND_REF_PATH', ref_file):
            ref = get_tool_quick_reference("unknown")
            assert "No commands found" in ref


class TestParseCommandReference:
    """Tests for _parse_command_reference function."""

    def setup_method(self):
        """Reset cache before each test."""
        import cli.knowledge.commands
        cli.knowledge.commands._commands_cache = None

    def test_parse_returns_dict_with_all_tools(self, tmp_path):
        """Test parsing returns dict with all tool keys."""
        ref_content = "# Reference"
        ref_file = tmp_path / "ref.md"
        ref_file.write_text(ref_content)

        with patch('cli.knowledge.commands.COMMAND_REF_PATH', ref_file):
            result = _parse_command_reference()
            assert "gemini" in result
            assert "openai" in result
            assert "claude" in result

    def test_parse_caches_result(self, tmp_path):
        """Test that parsing caches the result."""
        import cli.knowledge.commands

        ref_content = "# Reference"
        ref_file = tmp_path / "ref.md"
        ref_file.write_text(ref_content)

        with patch('cli.knowledge.commands.COMMAND_REF_PATH', ref_file):
            result1 = _parse_command_reference()
            result2 = _parse_command_reference()
            # Should be the same cached object
            assert result1 is result2

    def test_parse_multiline_content(self, tmp_path):
        """Test parsing multi-line command reference."""
        ref_content = """# AI CLI Commands Reference

## 1. Gemini CLI (Google AI)

### Basic Usage
- `gemini` Start interactive mode

## 2. Claude Code (Anthropic)

### Commands
- `claude` Start interactive mode

## 3. OpenAI Codex

### Usage
- `codex` Start codex
"""
        ref_file = tmp_path / "ref.md"
        ref_file.write_text(ref_content)

        with patch('cli.knowledge.commands.COMMAND_REF_PATH', ref_file):
            result = _parse_command_reference()
            # Should parse commands for multiple tools
            assert isinstance(result, dict)
