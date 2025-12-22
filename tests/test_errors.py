"""Tests for cli/errors.py module."""

import pytest

from cli.errors import (
    CLIError, ConfigError, ConfigNotFoundError, ConfigParseError,
    ConfigValidationError, ToolError, ToolNotFoundError,
    ToolNotAvailableError, ToolExecutionError, RoutingError,
    NoAvailableToolError, KnowledgeError, DocumentNotFoundError,
    IndexError, ValidationResult, validate_config_data, format_error_for_display
)


class TestCLIError:
    """Tests for base CLIError class."""

    def test_error_with_message(self):
        """Test creating error with message only."""
        error = CLIError("Something went wrong")
        assert error.message == "Something went wrong"
        assert error.hint is None
        assert str(error) == "Something went wrong"

    def test_error_with_hint(self):
        """Test creating error with hint."""
        error = CLIError("Something went wrong", hint="Try this fix")
        assert error.message == "Something went wrong"
        assert error.hint == "Try this fix"
        assert "Try this fix" in str(error)


class TestConfigErrors:
    """Tests for configuration error classes."""

    def test_config_not_found_error(self):
        """Test ConfigNotFoundError."""
        error = ConfigNotFoundError("/path/to/config.json")
        assert error.path == "/path/to/config.json"
        assert "config.json" in str(error)
        assert error.hint is not None

    def test_config_parse_error(self):
        """Test ConfigParseError."""
        error = ConfigParseError("/path/to/config.json", "Invalid syntax at line 5")
        assert error.path == "/path/to/config.json"
        assert error.detail == "Invalid syntax at line 5"
        assert "Invalid syntax" in str(error)

    def test_config_validation_error(self):
        """Test ConfigValidationError."""
        errors = ["Missing required key: 'roles'", "Invalid tool reference"]
        error = ConfigValidationError(errors)
        assert len(error.errors) == 2
        assert "Missing required key" in str(error)
        assert "Invalid tool reference" in str(error)


class TestToolErrors:
    """Tests for tool-related error classes."""

    def test_tool_not_found_error(self):
        """Test ToolNotFoundError."""
        error = ToolNotFoundError("claude", "claude")
        assert error.tool == "claude"
        assert error.command == "claude"
        assert "claude" in str(error)
        assert error.hint is not None

    def test_tool_not_available_error(self):
        """Test ToolNotAvailableError."""
        error = ToolNotAvailableError("gemini", "not authenticated")
        assert error.tool == "gemini"
        assert error.reason == "not authenticated"
        assert "not authenticated" in str(error)

    def test_tool_execution_error(self):
        """Test ToolExecutionError."""
        error = ToolExecutionError("claude", "claude -p test", 1, "Permission denied")
        assert error.tool == "claude"
        assert error.exit_code == 1
        assert error.stderr == "Permission denied"
        assert "exit code 1" in str(error)

    def test_tool_execution_error_without_stderr(self):
        """Test ToolExecutionError without stderr."""
        error = ToolExecutionError("claude", "claude", 1)
        assert error.stderr == ""
        assert "exit code 1" in str(error)


class TestRoutingErrors:
    """Tests for routing-related error classes."""

    def test_no_available_tool_error(self):
        """Test NoAvailableToolError."""
        error = NoAvailableToolError()
        assert "No AI tools" in str(error)
        assert error.hint is not None


class TestKnowledgeErrors:
    """Tests for knowledge module error classes."""

    def test_document_not_found_error(self):
        """Test DocumentNotFoundError."""
        error = DocumentNotFoundError("missing.md")
        assert error.name == "missing.md"
        assert "missing.md" in str(error)
        assert "/docs" in error.hint

    def test_index_error(self):
        """Test IndexError."""
        error = IndexError("Index corrupted")
        assert "Index corrupted" in str(error)
        assert "refresh" in error.hint


class TestValidationResult:
    """Tests for ValidationResult dataclass."""

    def test_success(self):
        """Test creating success result."""
        result = ValidationResult.success()
        assert result.valid is True
        assert result.errors == []
        assert result.warnings == []

    def test_failure(self):
        """Test creating failure result."""
        result = ValidationResult.failure(["Error 1", "Error 2"])
        assert result.valid is False
        assert len(result.errors) == 2
        assert result.warnings == []

    def test_failure_with_warnings(self):
        """Test creating failure result with warnings."""
        result = ValidationResult.failure(
            ["Error 1"],
            warnings=["Warning 1", "Warning 2"]
        )
        assert result.valid is False
        assert len(result.errors) == 1
        assert len(result.warnings) == 2


class TestValidateConfigData:
    """Tests for validate_config_data function."""

    def test_valid_config(self):
        """Test validating a complete valid config."""
        data = {
            "roles": {
                "research": {
                    "keywords": ["research", "find"],
                    "primary": "gemini",
                    "fallback": ["claude"]
                }
            },
            "tools": {
                "gemini": {"command": "gemini", "name": "Gemini"},
                "claude": {"command": "claude", "name": "Claude"}
            },
            "auth_status": {
                "gemini": True,
                "claude": True
            }
        }
        result = validate_config_data(data)
        assert result.valid is True
        assert result.errors == []

    def test_missing_required_keys(self):
        """Test validation fails with missing required keys."""
        data = {"roles": {}}  # Missing tools and auth_status
        result = validate_config_data(data)
        assert result.valid is False
        assert any("tools" in e for e in result.errors)
        assert any("auth_status" in e for e in result.errors)

    def test_empty_config(self):
        """Test validation with empty config."""
        data = {}
        result = validate_config_data(data)
        assert result.valid is False
        assert len(result.errors) == 3  # roles, tools, auth_status

    def test_role_missing_keywords(self):
        """Test validation fails when role missing keywords."""
        data = {
            "roles": {
                "research": {"primary": "gemini"}  # Missing keywords
            },
            "tools": {"gemini": {}},
            "auth_status": {}
        }
        result = validate_config_data(data)
        assert result.valid is False
        assert any("keywords" in e for e in result.errors)

    def test_role_missing_primary(self):
        """Test validation fails when role missing primary."""
        data = {
            "roles": {
                "research": {"keywords": ["research"]}  # Missing primary
            },
            "tools": {"gemini": {}},
            "auth_status": {}
        }
        result = validate_config_data(data)
        assert result.valid is False
        assert any("primary" in e for e in result.errors)

    def test_role_invalid_keywords_type(self):
        """Test validation fails when keywords not an array."""
        data = {
            "roles": {
                "research": {"keywords": "not-array", "primary": "gemini"}
            },
            "tools": {"gemini": {}},
            "auth_status": {}
        }
        result = validate_config_data(data)
        assert result.valid is False
        assert any("array" in e for e in result.errors)

    def test_role_references_unknown_tool(self):
        """Test validation fails when role references unknown tool."""
        data = {
            "roles": {
                "research": {"keywords": ["research"], "primary": "unknown"}
            },
            "tools": {"gemini": {}},
            "auth_status": {}
        }
        result = validate_config_data(data)
        assert result.valid is False
        assert any("unknown" in e for e in result.errors)

    def test_no_tools_defined(self):
        """Test validation fails with no tools."""
        data = {
            "roles": {},
            "tools": {},
            "auth_status": {}
        }
        result = validate_config_data(data)
        assert result.valid is False
        assert any("No tools" in e for e in result.errors)

    def test_warning_empty_keywords(self):
        """Test warning for empty keywords list."""
        data = {
            "roles": {
                "research": {"keywords": [], "primary": "gemini"}
            },
            "tools": {"gemini": {}},
            "auth_status": {"gemini": True}
        }
        result = validate_config_data(data)
        assert result.valid is True  # Still valid
        assert any("no keywords" in w for w in result.warnings)

    def test_warning_missing_auth_status(self):
        """Test warning for tool without auth_status."""
        data = {
            "roles": {},
            "tools": {"gemini": {}},
            "auth_status": {}  # Missing gemini auth
        }
        result = validate_config_data(data)
        # No roles so can't fail on missing keywords/primary
        # But should warn about missing auth_status
        assert any("auth_status" in w for w in result.warnings)

    def test_warning_fallback_unknown_tool(self):
        """Test warning for fallback referencing unknown tool."""
        data = {
            "roles": {
                "research": {
                    "keywords": ["research"],
                    "primary": "gemini",
                    "fallback": ["unknown"]
                }
            },
            "tools": {"gemini": {}},
            "auth_status": {"gemini": True}
        }
        result = validate_config_data(data)
        assert result.valid is True  # Warning, not error
        assert any("unknown" in w for w in result.warnings)


class TestFormatErrorForDisplay:
    """Tests for format_error_for_display function."""

    def test_format_simple_error(self):
        """Test formatting simple error."""
        error = CLIError("Something went wrong")
        formatted = format_error_for_display(error)
        assert "Error" in formatted
        assert "Something went wrong" in formatted

    def test_format_error_with_hint(self):
        """Test formatting error with hint."""
        error = CLIError("Something went wrong", hint="Try this")
        formatted = format_error_for_display(error)
        assert "Something went wrong" in formatted
        assert "Hint" in formatted
        assert "Try this" in formatted

    def test_format_config_error(self):
        """Test formatting ConfigError."""
        error = ConfigNotFoundError("/path/to/file")
        formatted = format_error_for_display(error)
        assert "Error" in formatted
        assert "/path/to/file" in formatted


class TestErrorHierarchy:
    """Tests for error class hierarchy."""

    def test_config_errors_inherit_cli_error(self):
        """Test ConfigError classes inherit from CLIError."""
        assert issubclass(ConfigError, CLIError)
        assert issubclass(ConfigNotFoundError, ConfigError)
        assert issubclass(ConfigParseError, ConfigError)
        assert issubclass(ConfigValidationError, ConfigError)

    def test_tool_errors_inherit_cli_error(self):
        """Test ToolError classes inherit from CLIError."""
        assert issubclass(ToolError, CLIError)
        assert issubclass(ToolNotFoundError, ToolError)
        assert issubclass(ToolNotAvailableError, ToolError)
        assert issubclass(ToolExecutionError, ToolError)

    def test_routing_errors_inherit_cli_error(self):
        """Test RoutingError classes inherit from CLIError."""
        assert issubclass(RoutingError, CLIError)
        assert issubclass(NoAvailableToolError, RoutingError)

    def test_knowledge_errors_inherit_cli_error(self):
        """Test KnowledgeError classes inherit from CLIError."""
        assert issubclass(KnowledgeError, CLIError)
        assert issubclass(DocumentNotFoundError, KnowledgeError)

    def test_catch_by_base_class(self):
        """Test errors can be caught by base class."""
        error = ConfigNotFoundError("/path")
        assert isinstance(error, CLIError)
        assert isinstance(error, ConfigError)
        assert isinstance(error, Exception)
