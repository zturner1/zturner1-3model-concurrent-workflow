"""Shared test fixtures for Terminal AI Workflow CLI."""

import json
import pytest
from pathlib import Path
from typing import Dict, Any


@pytest.fixture
def sample_role_config() -> Dict[str, Any]:
    """Sample role configuration for testing."""
    return {
        "roles": {
            "research": {
                "description": "Scout & Researcher",
                "keywords": ["research", "find", "search", "explore"],
                "primary": "gemini",
                "fallback": ["claude", "openai"]
            },
            "analysis": {
                "description": "Auditor",
                "keywords": ["analyze", "review", "audit"],
                "primary": "openai",
                "fallback": ["claude"]
            },
            "deep_work": {
                "description": "Builder & Architect",
                "keywords": ["build", "create", "implement", "fix"],
                "primary": "claude",
                "fallback": ["openai"]
            }
        },
        "tools": {
            "claude": {
                "name": "Claude Code",
                "command": "claude",
                "context_file": "CLAUDE.md",
                "role": "Builder & Architect"
            },
            "gemini": {
                "name": "Gemini CLI",
                "command": "gemini",
                "context_file": "GEMINI.md",
                "role": "Scout & Researcher"
            },
            "openai": {
                "name": "OpenAI Codex",
                "command": "codex",
                "context_file": "OPENAI.md",
                "role": "Auditor"
            }
        },
        "auth_status": {
            "claude": True,
            "gemini": True,
            "openai": True
        }
    }


@pytest.fixture
def temp_config_file(tmp_path: Path, sample_role_config: Dict[str, Any]) -> Path:
    """Create a temporary config file for testing."""
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    config_file = config_dir / "role_config.json"
    config_file.write_text(json.dumps(sample_role_config, indent=2))
    return config_file


@pytest.fixture
def temp_docs_library(tmp_path: Path) -> Path:
    """Create a temporary docs/library with sample documents."""
    docs_dir = tmp_path / "docs" / "library"
    docs_dir.mkdir(parents=True)

    # Create sample markdown file
    (docs_dir / "test_commands.md").write_text("""# Test Commands Reference

## 1. Claude CLI

### Commands
- `claude` Start interactive mode
- `claude -p "query"` Print mode

## 2. Gemini CLI

### Commands
- `gemini` Start interactive mode
- `gemini -p "query"` One-shot prompt
""")

    # Create sample workflow file
    (docs_dir / "Workflow_Strategy.md").write_text("""# Workflow Strategy

## 1. Gemini: The Scout & Researcher
- Role: Information gathering

## 2. Claude: The Builder & Architect
- Role: Implementation

## 3. OpenAI: The Auditor
- Role: Review
""")

    return docs_dir


@pytest.fixture
def sample_sentences() -> list:
    """Sample sentences for routing tests."""
    return [
        ("research AI trends", "gemini"),
        ("find the API documentation", "gemini"),
        ("build a hello world script", "claude"),
        ("create a new feature", "claude"),
        ("review the code", "openai"),
        ("analyze this architecture", "openai"),
        ("hello world", "claude"),  # Default routing
    ]
