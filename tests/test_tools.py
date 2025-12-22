"""Tests for cli/tools.py module."""

import pytest
from unittest.mock import patch, MagicMock

from cli.tools import (
    ToolStatus, check_tool_installed, get_tool_status,
    get_all_tools_status, require_tool, get_available_tools,
    get_best_available_tool, format_tools_status_table
)
from cli.errors import ToolNotFoundError, ToolNotAvailableError
from cli.config import _reset_config


class TestToolStatus:
    """Tests for ToolStatus dataclass."""

    def test_tool_status_creation(self):
        """Test creating a ToolStatus instance."""
        status = ToolStatus(
            name="Claude Code",
            tool_id="claude",
            command="claude",
            installed=True,
            authenticated=True,
            available=True,
            version="1.0.0"
        )
        assert status.name == "Claude Code"
        assert status.available is True
        assert status.version == "1.0.0"

    def test_tool_status_with_error(self):
        """Test ToolStatus with error."""
        status = ToolStatus(
            name="Claude",
            tool_id="claude",
            command="claude",
            installed=False,
            authenticated=False,
            available=False,
            error="Command not found"
        )
        assert status.error == "Command not found"
        assert status.version is None


class TestCheckToolInstalled:
    """Tests for check_tool_installed function."""

    def test_tool_not_in_path(self):
        """Test checking tool not in PATH."""
        with patch('shutil.which', return_value=None):
            installed, error = check_tool_installed("nonexistent")
            assert installed is False
            assert "not found" in error

    def test_tool_in_path_version_success(self):
        """Test checking tool that returns version."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "claude 1.2.3\n"

        with patch('shutil.which', return_value="/usr/bin/claude"):
            with patch('subprocess.run', return_value=mock_result):
                installed, version = check_tool_installed("claude")
                assert installed is True
                assert "1.2.3" in version

    def test_tool_in_path_version_fails(self):
        """Test checking tool where --version fails."""
        mock_result = MagicMock()
        mock_result.returncode = 1

        with patch('shutil.which', return_value="/usr/bin/claude"):
            with patch('subprocess.run', return_value=mock_result):
                installed, version = check_tool_installed("claude")
                assert installed is True
                assert version is None  # Version unknown but installed


class TestGetToolStatus:
    """Tests for get_tool_status function."""

    def setup_method(self):
        """Reset config before each test."""
        _reset_config()

    def teardown_method(self):
        """Reset config after each test."""
        _reset_config()

    def test_get_status_available_tool(self, temp_config_file, monkeypatch):
        """Test getting status for available tool."""
        monkeypatch.chdir(temp_config_file.parent.parent)

        with patch('cli.tools.check_tool_installed', return_value=(True, "1.0")):
            status = get_tool_status("claude")
            assert status.tool_id == "claude"
            assert status.installed is True
            assert status.authenticated is True
            assert status.available is True

    def test_get_status_not_installed(self, temp_config_file, monkeypatch):
        """Test getting status for non-installed tool."""
        monkeypatch.chdir(temp_config_file.parent.parent)

        with patch('cli.tools.check_tool_installed', return_value=(False, "not found")):
            status = get_tool_status("claude")
            assert status.installed is False
            assert status.available is False

    def test_get_status_unknown_tool(self, temp_config_file, monkeypatch):
        """Test getting status for unknown tool."""
        monkeypatch.chdir(temp_config_file.parent.parent)

        status = get_tool_status("unknown_tool")
        assert status.available is False
        assert "not defined" in status.error


class TestGetAllToolsStatus:
    """Tests for get_all_tools_status function."""

    def setup_method(self):
        """Reset config before each test."""
        _reset_config()

    def teardown_method(self):
        """Reset config after each test."""
        _reset_config()

    def test_returns_all_tools(self, temp_config_file, monkeypatch):
        """Test that all configured tools are returned."""
        monkeypatch.chdir(temp_config_file.parent.parent)

        with patch('cli.tools.check_tool_installed', return_value=(True, "1.0")):
            statuses = get_all_tools_status()
            tool_ids = {s.tool_id for s in statuses}
            assert "claude" in tool_ids
            assert "gemini" in tool_ids
            assert "openai" in tool_ids


class TestRequireTool:
    """Tests for require_tool function."""

    def setup_method(self):
        """Reset config before each test."""
        _reset_config()

    def teardown_method(self):
        """Reset config after each test."""
        _reset_config()

    def test_require_available_tool(self, temp_config_file, monkeypatch):
        """Test requiring available tool succeeds."""
        monkeypatch.chdir(temp_config_file.parent.parent)

        with patch('cli.tools.check_tool_installed', return_value=(True, "1.0")):
            status = require_tool("claude")
            assert status.available is True

    def test_require_not_installed_raises(self, temp_config_file, monkeypatch):
        """Test requiring non-installed tool raises ToolNotFoundError."""
        monkeypatch.chdir(temp_config_file.parent.parent)

        with patch('cli.tools.check_tool_installed', return_value=(False, "not found")):
            with pytest.raises(ToolNotFoundError):
                require_tool("claude")

    def test_require_not_authenticated_raises(self, temp_config_file, sample_role_config, monkeypatch):
        """Test requiring non-authenticated tool raises ToolNotAvailableError."""
        import json
        sample_role_config["auth_status"]["claude"] = False
        temp_config_file.write_text(json.dumps(sample_role_config))
        monkeypatch.chdir(temp_config_file.parent.parent)

        with patch('cli.tools.check_tool_installed', return_value=(True, "1.0")):
            with pytest.raises(ToolNotAvailableError):
                require_tool("claude")


class TestGetAvailableTools:
    """Tests for get_available_tools function."""

    def setup_method(self):
        """Reset config before each test."""
        _reset_config()

    def teardown_method(self):
        """Reset config after each test."""
        _reset_config()

    def test_returns_available_tools(self, temp_config_file, monkeypatch):
        """Test returns list of available tool IDs."""
        monkeypatch.chdir(temp_config_file.parent.parent)

        with patch('cli.tools.check_tool_installed', return_value=(True, "1.0")):
            available = get_available_tools()
            assert isinstance(available, list)
            assert "claude" in available


class TestGetBestAvailableTool:
    """Tests for get_best_available_tool function."""

    def setup_method(self):
        """Reset config before each test."""
        _reset_config()

    def teardown_method(self):
        """Reset config after each test."""
        _reset_config()

    def test_returns_first_available(self, temp_config_file, monkeypatch):
        """Test returns first available tool from preference list."""
        monkeypatch.chdir(temp_config_file.parent.parent)

        with patch('cli.tools.check_tool_installed', return_value=(True, "1.0")):
            best = get_best_available_tool(["gemini", "claude"])
            assert best in ["gemini", "claude"]

    def test_returns_none_if_none_available(self, temp_config_file, monkeypatch):
        """Test returns None if no tools available."""
        monkeypatch.chdir(temp_config_file.parent.parent)

        with patch('cli.tools.check_tool_installed', return_value=(False, "not found")):
            best = get_best_available_tool(["gemini", "claude"])
            assert best is None


class TestFormatToolsStatusTable:
    """Tests for format_tools_status_table function."""

    def test_formats_single_tool(self):
        """Test formatting single tool status."""
        statuses = [
            ToolStatus(
                name="Claude Code",
                tool_id="claude",
                command="claude",
                installed=True,
                authenticated=True,
                available=True,
                version="1.0.0"
            )
        ]
        table = format_tools_status_table(statuses)
        assert "Claude Code" in table
        assert "Yes" in table  # Installed
        assert "Ready" in table  # Available
        assert "1.0.0" in table

    def test_formats_unavailable_tool(self):
        """Test formatting unavailable tool."""
        statuses = [
            ToolStatus(
                name="Gemini",
                tool_id="gemini",
                command="gemini",
                installed=False,
                authenticated=False,
                available=False,
                error="Command not found"
            )
        ]
        table = format_tools_status_table(statuses)
        assert "Gemini" in table
        assert "No" in table
        assert "Unavailable" in table
        assert "Command not found" in table

    def test_formats_multiple_tools(self):
        """Test formatting multiple tools."""
        statuses = [
            ToolStatus("Claude", "claude", "claude", True, True, True),
            ToolStatus("Gemini", "gemini", "gemini", True, False, False),
            ToolStatus("OpenAI", "openai", "codex", False, False, False),
        ]
        table = format_tools_status_table(statuses)
        assert "Claude" in table
        assert "Gemini" in table
        assert "OpenAI" in table

    def test_table_has_header(self):
        """Test table includes header row."""
        statuses = [
            ToolStatus("Claude", "claude", "claude", True, True, True)
        ]
        table = format_tools_status_table(statuses)
        assert "Tool" in table
        assert "Command" in table
        assert "Status" in table
