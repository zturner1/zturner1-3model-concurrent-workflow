"""Tests for cli/router.py module."""

import json
import pytest
from unittest.mock import patch, MagicMock

from cli.router import (
    Route, split_sentences, get_first_word, find_keyword_match,
    route_sentence, route_input, consolidate_routes
)
from cli.config import Config, RoleConfig, ToolConfig, _reset_config


class TestRoute:
    """Tests for Route dataclass."""

    def test_route_creation(self):
        """Test creating a Route instance."""
        route = Route(
            tool="claude",
            task="build a feature",
            tool_display_name="Claude Code"
        )
        assert route.tool == "claude"
        assert route.task == "build a feature"
        assert route.tool_display_name == "Claude Code"


class TestSplitSentences:
    """Tests for split_sentences function."""

    def test_single_sentence(self):
        """Test splitting a single sentence."""
        result = split_sentences("Build a new feature")
        assert result == ["Build a new feature"]

    def test_multiple_sentences_period(self):
        """Test splitting sentences with periods."""
        result = split_sentences("Research the API. Build the integration.")
        assert result == ["Research the API", "Build the integration"]

    def test_multiple_sentences_exclamation(self):
        """Test splitting sentences with exclamation marks."""
        result = split_sentences("Find the bug! Fix it immediately!")
        assert result == ["Find the bug", "Fix it immediately"]

    def test_multiple_sentences_question(self):
        """Test splitting sentences with question marks."""
        result = split_sentences("What is the issue? How do we fix it?")
        assert result == ["What is the issue", "How do we fix it"]

    def test_mixed_punctuation(self):
        """Test splitting sentences with mixed punctuation."""
        result = split_sentences("Search for docs. Is this right? Do it!")
        assert result == ["Search for docs", "Is this right", "Do it"]

    def test_empty_string(self):
        """Test splitting an empty string."""
        result = split_sentences("")
        assert result == []

    def test_whitespace_only(self):
        """Test splitting whitespace-only string."""
        result = split_sentences("   ")
        assert result == []

    def test_trailing_punctuation(self):
        """Test sentence with trailing punctuation."""
        result = split_sentences("Build a feature...")
        assert result == ["Build a feature"]


class TestGetFirstWord:
    """Tests for get_first_word function."""

    def test_simple_sentence(self):
        """Test getting first word from simple sentence."""
        assert get_first_word("Build a feature") == "build"

    def test_lowercase_conversion(self):
        """Test first word is converted to lowercase."""
        assert get_first_word("RESEARCH the topic") == "research"

    def test_empty_string(self):
        """Test getting first word from empty string."""
        assert get_first_word("") == ""

    def test_whitespace_only(self):
        """Test getting first word from whitespace string."""
        assert get_first_word("   ") == ""

    def test_single_word(self):
        """Test getting first word from single word."""
        assert get_first_word("Hello") == "hello"


class TestFindKeywordMatch:
    """Tests for find_keyword_match function."""

    def test_first_word_match(self):
        """Test matching keyword at first word position."""
        keywords = ["research", "find", "search"]
        assert find_keyword_match("research the topic", keywords) == "research"

    def test_keyword_in_middle(self):
        """Test matching keyword in middle of sentence."""
        keywords = ["research", "find", "search"]
        assert find_keyword_match("please research the topic", keywords) == "research"

    def test_keyword_at_end(self):
        """Test matching keyword at end of sentence."""
        keywords = ["research", "api"]
        assert find_keyword_match("I need to do research", keywords) == "research"

    def test_no_match(self):
        """Test when no keyword matches."""
        keywords = ["research", "find"]
        assert find_keyword_match("build a feature", keywords) is None

    def test_case_insensitive(self):
        """Test matching is case-insensitive."""
        keywords = ["Research", "Find"]
        assert find_keyword_match("RESEARCH the topic", keywords) == "Research"

    def test_first_word_priority(self):
        """Test that first word match takes priority."""
        keywords = ["find", "research"]
        # "find" is first word, should match even if "research" appears later
        result = find_keyword_match("find something to research", keywords)
        assert result == "find"

    def test_whole_word_matching(self):
        """Test that keyword matches whole words only."""
        keywords = ["search"]
        # "searching" contains "search" but shouldn't match
        assert find_keyword_match("I am searching for docs", keywords) is None

    def test_word_boundary_match(self):
        """Test keyword matches at word boundaries."""
        keywords = ["search"]
        assert find_keyword_match("please search now", keywords) == "search"

    def test_empty_keywords(self):
        """Test with empty keywords list."""
        assert find_keyword_match("any sentence", []) is None

    def test_empty_sentence(self):
        """Test with empty sentence."""
        keywords = ["research"]
        assert find_keyword_match("", keywords) is None


class TestRouteSetence:
    """Tests for route_sentence function."""

    def setup_method(self):
        """Reset config before each test."""
        _reset_config()

    def teardown_method(self):
        """Reset config after each test."""
        _reset_config()

    def test_routes_to_research_tool(self, temp_config_file, monkeypatch):
        """Test sentence routes to research tool (gemini)."""
        monkeypatch.chdir(temp_config_file.parent.parent)

        route = route_sentence("research AI trends")
        assert route.tool == "gemini"
        assert route.task == "research AI trends"

    def test_routes_to_deep_work_tool(self, temp_config_file, monkeypatch):
        """Test sentence routes to deep work tool (claude)."""
        monkeypatch.chdir(temp_config_file.parent.parent)

        route = route_sentence("build a new feature")
        assert route.tool == "claude"
        assert route.task == "build a new feature"

    def test_routes_to_analysis_tool(self, temp_config_file, monkeypatch):
        """Test sentence routes to analysis tool (openai)."""
        monkeypatch.chdir(temp_config_file.parent.parent)

        route = route_sentence("analyze the code")
        assert route.tool == "openai"
        assert route.task == "analyze the code"

    def test_default_routing(self, temp_config_file, monkeypatch):
        """Test default routing when no keyword matches."""
        monkeypatch.chdir(temp_config_file.parent.parent)

        route = route_sentence("hello world")
        assert route.tool == "claude"  # Default

    def test_fallback_when_primary_unavailable(self, temp_config_file, sample_role_config, monkeypatch):
        """Test fallback tool when primary is unavailable."""
        # Make gemini unavailable
        sample_role_config["auth_status"]["gemini"] = False
        temp_config_file.write_text(json.dumps(sample_role_config))
        monkeypatch.chdir(temp_config_file.parent.parent)

        route = route_sentence("research AI trends")
        # Should fall back to claude (first fallback for research)
        assert route.tool == "claude"

    def test_display_name_included(self, temp_config_file, monkeypatch):
        """Test that display name is included in route."""
        monkeypatch.chdir(temp_config_file.parent.parent)

        route = route_sentence("build a feature")
        assert route.tool_display_name == "Claude Code"


class TestRouteInput:
    """Tests for route_input function."""

    def setup_method(self):
        """Reset config before each test."""
        _reset_config()

    def teardown_method(self):
        """Reset config after each test."""
        _reset_config()

    def test_single_sentence(self, temp_config_file, monkeypatch):
        """Test routing a single sentence."""
        monkeypatch.chdir(temp_config_file.parent.parent)

        routes = route_input("build a feature")
        assert len(routes) == 1
        assert routes[0].tool == "claude"

    def test_multiple_sentences(self, temp_config_file, monkeypatch):
        """Test routing multiple sentences."""
        monkeypatch.chdir(temp_config_file.parent.parent)

        routes = route_input("research AI trends. build a prototype.")
        assert len(routes) == 2
        assert routes[0].tool == "gemini"
        assert routes[1].tool == "claude"

    def test_empty_input(self, temp_config_file, monkeypatch):
        """Test routing empty input."""
        monkeypatch.chdir(temp_config_file.parent.parent)

        routes = route_input("")
        assert len(routes) == 1  # Treats empty as one task

    def test_different_tools_different_sentences(self, temp_config_file, monkeypatch):
        """Test that different sentences route to different tools."""
        monkeypatch.chdir(temp_config_file.parent.parent)

        routes = route_input("find the docs. implement the feature. review the code.")
        assert len(routes) == 3
        assert routes[0].tool == "gemini"  # find -> research
        assert routes[1].tool == "claude"  # implement -> deep_work
        assert routes[2].tool == "openai"  # review -> analysis


class TestConsolidateRoutes:
    """Tests for consolidate_routes function."""

    def test_consolidate_same_tool(self):
        """Test consolidating routes with same tool."""
        routes = [
            Route(tool="claude", task="build feature A", tool_display_name="Claude"),
            Route(tool="claude", task="build feature B", tool_display_name="Claude"),
        ]
        result = consolidate_routes(routes)
        assert len(result) == 1
        assert result[0].tool == "claude"
        assert "build feature A" in result[0].task
        assert "build feature B" in result[0].task

    def test_consolidate_different_tools(self):
        """Test consolidating routes with different tools."""
        routes = [
            Route(tool="claude", task="build feature", tool_display_name="Claude"),
            Route(tool="gemini", task="research topic", tool_display_name="Gemini"),
        ]
        result = consolidate_routes(routes)
        assert len(result) == 2

    def test_consolidate_mixed(self):
        """Test consolidating mixed routes."""
        routes = [
            Route(tool="claude", task="task 1", tool_display_name="Claude"),
            Route(tool="gemini", task="task 2", tool_display_name="Gemini"),
            Route(tool="claude", task="task 3", tool_display_name="Claude"),
        ]
        result = consolidate_routes(routes)
        assert len(result) == 2
        # Find the claude route
        claude_route = next(r for r in result if r.tool == "claude")
        assert "task 1" in claude_route.task
        assert "task 3" in claude_route.task

    def test_consolidate_empty(self):
        """Test consolidating empty list."""
        result = consolidate_routes([])
        assert result == []

    def test_task_separator(self):
        """Test that tasks are separated by period and space."""
        routes = [
            Route(tool="claude", task="task A", tool_display_name="Claude"),
            Route(tool="claude", task="task B", tool_display_name="Claude"),
        ]
        result = consolidate_routes(routes)
        assert result[0].task == "task A. task B"


class TestRoutingIntegration:
    """Integration tests for full routing workflow."""

    def setup_method(self):
        """Reset config before each test."""
        _reset_config()

    def teardown_method(self):
        """Reset config after each test."""
        _reset_config()

    def test_sample_routing_scenarios(self, temp_config_file, sample_sentences, monkeypatch):
        """Test routing with sample sentences from fixture."""
        monkeypatch.chdir(temp_config_file.parent.parent)

        for sentence, expected_tool in sample_sentences:
            route = route_sentence(sentence)
            assert route.tool == expected_tool, f"'{sentence}' should route to {expected_tool}, got {route.tool}"

    def test_full_workflow(self, temp_config_file, monkeypatch):
        """Test complete routing workflow."""
        monkeypatch.chdir(temp_config_file.parent.parent)

        # Simulate a complex user input
        text = "Research the best practices. Build the implementation. Review the result."

        # Route all sentences
        routes = route_input(text)
        assert len(routes) == 3

        # Consolidate routes
        consolidated = consolidate_routes(routes)

        # Should have 3 different tools
        tools = {r.tool for r in consolidated}
        assert tools == {"gemini", "claude", "openai"}
