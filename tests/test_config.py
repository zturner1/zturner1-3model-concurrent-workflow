"""Tests for cli/config.py module."""

import json
import pytest
from pathlib import Path

from cli.config import (
    Config, RoleConfig, ToolConfig,
    load_config, get_config, _reset_config
)
from cli.errors import ConfigNotFoundError, ConfigParseError, ConfigValidationError


class TestToolConfig:
    """Tests for ToolConfig dataclass."""

    def test_tool_config_creation(self):
        """Test creating a ToolConfig instance."""
        config = ToolConfig(
            name="Test Tool",
            command="test-cmd",
            context_file="TEST.md"
        )
        assert config.name == "Test Tool"
        assert config.command == "test-cmd"
        assert config.context_file == "TEST.md"
        assert config.role == ""  # Default value

    def test_tool_config_with_role(self):
        """Test ToolConfig with optional role field."""
        config = ToolConfig(
            name="Test Tool",
            command="test-cmd",
            context_file="TEST.md",
            role="Builder"
        )
        assert config.role == "Builder"


class TestRoleConfig:
    """Tests for RoleConfig dataclass."""

    def test_role_config_creation(self):
        """Test creating a RoleConfig instance."""
        config = RoleConfig(
            keywords=["test", "check"],
            primary="claude",
            fallback=["openai"],
            description="Test role"
        )
        assert config.description == "Test role"
        assert "test" in config.keywords
        assert config.primary == "claude"
        assert "openai" in config.fallback

    def test_role_config_defaults(self):
        """Test RoleConfig with default values."""
        config = RoleConfig(
            keywords=["test"],
            primary="claude"
        )
        assert config.fallback == []
        assert config.description == ""


class TestConfigLoad:
    """Tests for Config.load() class method."""

    def test_load_from_file(self, temp_config_file):
        """Test loading config from a valid JSON file."""
        config = Config.load(temp_config_file)

        assert isinstance(config, Config)
        assert "research" in config.roles
        assert "claude" in config.tools

    def test_load_roles_parsed(self, temp_config_file):
        """Test that roles are properly parsed into RoleConfig objects."""
        config = Config.load(temp_config_file)

        research_role = config.roles["research"]
        assert isinstance(research_role, RoleConfig)
        assert research_role.primary == "gemini"
        assert "find" in research_role.keywords

    def test_load_tools_parsed(self, temp_config_file):
        """Test that tools are properly parsed into ToolConfig objects."""
        config = Config.load(temp_config_file)

        claude_tool = config.tools["claude"]
        assert isinstance(claude_tool, ToolConfig)
        assert claude_tool.name == "Claude Code"
        assert claude_tool.command == "claude"

    def test_load_auth_status(self, temp_config_file):
        """Test that auth_status is properly loaded."""
        config = Config.load(temp_config_file)

        assert config.auth_status["claude"] is True
        assert config.auth_status["gemini"] is True

    def test_load_file_not_found(self, tmp_path):
        """Test loading config from non-existent file raises error."""
        fake_path = tmp_path / "nonexistent.json"

        with pytest.raises(ConfigNotFoundError) as exc_info:
            Config.load(fake_path)
        assert "nonexistent.json" in str(exc_info.value)

    def test_load_invalid_json(self, tmp_path):
        """Test loading config from invalid JSON raises error."""
        bad_file = tmp_path / "bad.json"
        bad_file.write_text("{ invalid json }")

        with pytest.raises(ConfigParseError) as exc_info:
            Config.load(bad_file)
        assert "bad.json" in str(exc_info.value)


class TestConfigMethods:
    """Tests for Config instance methods."""

    def test_is_tool_available_true(self, temp_config_file):
        """Test is_tool_available returns True for available tools."""
        config = Config.load(temp_config_file)
        assert config.is_tool_available("claude") is True
        assert config.is_tool_available("gemini") is True

    def test_is_tool_available_false(self, temp_config_file, sample_role_config):
        """Test is_tool_available returns False for unavailable tools."""
        # Modify the config file
        sample_role_config["auth_status"]["claude"] = False
        temp_config_file.write_text(json.dumps(sample_role_config))

        config = Config.load(temp_config_file)
        assert config.is_tool_available("claude") is False

    def test_is_tool_available_unknown(self, temp_config_file):
        """Test is_tool_available returns False for unknown tools."""
        config = Config.load(temp_config_file)
        assert config.is_tool_available("unknown_tool") is False

    def test_get_tool_command(self, temp_config_file):
        """Test get_tool_command returns correct command."""
        config = Config.load(temp_config_file)
        assert config.get_tool_command("claude") == "claude"
        assert config.get_tool_command("openai") == "codex"

    def test_get_tool_command_fallback(self, temp_config_file):
        """Test get_tool_command falls back to tool name."""
        config = Config.load(temp_config_file)
        assert config.get_tool_command("unknown") == "unknown"


class TestLoadConfigFunction:
    """Tests for load_config helper function."""

    def test_load_config_from_path(self, temp_config_file):
        """Test load_config loads from specified path."""
        config = load_config(temp_config_file)
        assert isinstance(config, Config)
        assert "claude" in config.tools


class TestGetConfig:
    """Tests for get_config singleton function."""

    def setup_method(self):
        """Reset config before each test."""
        _reset_config()

    def teardown_method(self):
        """Reset config after each test."""
        _reset_config()

    def test_get_config_returns_config(self):
        """Test get_config returns a Config instance."""
        config = get_config()
        assert isinstance(config, Config)

    def test_get_config_singleton(self):
        """Test get_config returns same instance on multiple calls."""
        config1 = get_config()
        config2 = get_config()
        assert config1 is config2

    def test_reset_config_clears_singleton(self):
        """Test _reset_config clears the singleton."""
        config1 = get_config()
        _reset_config()
        # After reset, get_config will reload from file
        config2 = get_config()
        assert isinstance(config2, Config)
