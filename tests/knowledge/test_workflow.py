"""Tests for cli/knowledge/workflow.py module."""

import pytest

from cli.knowledge.workflow import (
    RoleInfo, ROLES, HANDOFF_ADVICE,
    get_role_info, get_all_roles, get_workflow_overview,
    get_handoff_advice, get_workflow_diagram
)


class TestRoleInfo:
    """Tests for RoleInfo dataclass."""

    def test_role_info_creation(self):
        """Test creating a RoleInfo instance."""
        role = RoleInfo(
            tool_id="test",
            name="Test Tool",
            role_title="Test Role",
            description="Test description",
            key_strengths=["strength1", "strength2"],
            typical_tasks=["task1", "task2"],
            deliverable="Test deliverable"
        )
        assert role.tool_id == "test"
        assert role.name == "Test Tool"
        assert len(role.key_strengths) == 2
        assert role.usage_note is None

    def test_role_info_with_usage_note(self):
        """Test RoleInfo with optional usage note."""
        role = RoleInfo(
            tool_id="test",
            name="Test",
            role_title="Test",
            description="Test",
            key_strengths=[],
            typical_tasks=[],
            deliverable="Test",
            usage_note="Reserve this tool"
        )
        assert role.usage_note == "Reserve this tool"


class TestROLES:
    """Tests for ROLES constant."""

    def test_roles_has_all_tools(self):
        """Test that ROLES contains all three tools."""
        assert "gemini" in ROLES
        assert "claude" in ROLES
        assert "openai" in ROLES

    def test_roles_gemini(self):
        """Test Gemini role definition."""
        gemini = ROLES["gemini"]
        assert gemini.tool_id == "gemini"
        assert gemini.role_title == "The Scout & Researcher"
        assert "Web search" in gemini.key_strengths

    def test_roles_claude(self):
        """Test Claude role definition."""
        claude = ROLES["claude"]
        assert claude.tool_id == "claude"
        assert claude.role_title == "The Builder & Architect"
        assert "Agentic file editing" in claude.key_strengths

    def test_roles_openai(self):
        """Test OpenAI role definition."""
        openai = ROLES["openai"]
        assert openai.tool_id == "openai"
        assert openai.role_title == "The Auditor"
        assert openai.usage_note is not None  # Has usage note


class TestHANDOFF_ADVICE:
    """Tests for HANDOFF_ADVICE constant."""

    def test_handoff_gemini_to_claude(self):
        """Test Gemini to Claude handoff advice exists."""
        assert ("gemini", "claude") in HANDOFF_ADVICE
        advice = HANDOFF_ADVICE[("gemini", "claude")]
        assert "Research Brief" in advice

    def test_handoff_claude_to_openai(self):
        """Test Claude to OpenAI handoff advice exists."""
        assert ("claude", "openai") in HANDOFF_ADVICE
        advice = HANDOFF_ADVICE[("claude", "openai")]
        assert "Audit" in advice

    def test_handoff_claude_to_gemini(self):
        """Test Claude to Gemini handoff advice exists."""
        assert ("claude", "gemini") in HANDOFF_ADVICE
        advice = HANDOFF_ADVICE[("claude", "gemini")]
        assert "Research" in advice

    def test_handoff_openai_to_claude(self):
        """Test OpenAI to Claude handoff advice exists."""
        assert ("openai", "claude") in HANDOFF_ADVICE
        advice = HANDOFF_ADVICE[("openai", "claude")]
        assert "Recommendations" in advice


class TestGetRoleInfo:
    """Tests for get_role_info function."""

    def test_get_role_claude(self):
        """Test getting Claude role info."""
        role = get_role_info("claude")
        assert role is not None
        assert role.tool_id == "claude"
        assert role.name == "Claude Code"

    def test_get_role_gemini(self):
        """Test getting Gemini role info."""
        role = get_role_info("gemini")
        assert role is not None
        assert role.tool_id == "gemini"

    def test_get_role_openai(self):
        """Test getting OpenAI role info."""
        role = get_role_info("openai")
        assert role is not None
        assert role.tool_id == "openai"

    def test_get_role_case_insensitive(self):
        """Test role lookup is case-insensitive."""
        role1 = get_role_info("claude")
        role2 = get_role_info("CLAUDE")
        role3 = get_role_info("Claude")
        assert role1 == role2 == role3

    def test_get_role_codex_alias(self):
        """Test 'codex' maps to OpenAI."""
        role = get_role_info("codex")
        assert role is not None
        assert role.tool_id == "openai"

    def test_get_role_gpt_alias(self):
        """Test 'gpt' maps to OpenAI."""
        role = get_role_info("gpt")
        assert role is not None
        assert role.tool_id == "openai"

    def test_get_role_anthropic_alias(self):
        """Test 'anthropic' maps to Claude."""
        role = get_role_info("anthropic")
        assert role is not None
        assert role.tool_id == "claude"

    def test_get_role_google_alias(self):
        """Test 'google' maps to Gemini."""
        role = get_role_info("google")
        assert role is not None
        assert role.tool_id == "gemini"

    def test_get_role_unknown(self):
        """Test getting unknown role returns None."""
        role = get_role_info("unknown_tool")
        assert role is None


class TestGetAllRoles:
    """Tests for get_all_roles function."""

    def test_returns_three_roles(self):
        """Test that all roles are returned."""
        roles = get_all_roles()
        assert len(roles) == 3

    def test_roles_are_role_info(self):
        """Test that all items are RoleInfo instances."""
        roles = get_all_roles()
        for role in roles:
            assert isinstance(role, RoleInfo)

    def test_roles_contain_all_tools(self):
        """Test that all tool IDs are represented."""
        roles = get_all_roles()
        tool_ids = {r.tool_id for r in roles}
        assert tool_ids == {"gemini", "claude", "openai"}


class TestGetWorkflowOverview:
    """Tests for get_workflow_overview function."""

    def test_returns_string(self):
        """Test that overview returns a string."""
        overview = get_workflow_overview()
        assert isinstance(overview, str)

    def test_contains_workflow_title(self):
        """Test overview contains workflow title."""
        overview = get_workflow_overview()
        assert "3-Model Workflow" in overview or "Workflow" in overview

    def test_contains_all_tools(self):
        """Test overview mentions all tools."""
        overview = get_workflow_overview()
        assert "Gemini" in overview
        assert "Claude" in overview
        assert "OpenAI" in overview

    def test_contains_role_descriptions(self):
        """Test overview contains role descriptions."""
        overview = get_workflow_overview()
        assert "Scout" in overview or "Research" in overview
        assert "Builder" in overview or "Implementation" in overview
        assert "Auditor" in overview or "Audit" in overview

    def test_contains_diagram(self):
        """Test overview contains workflow diagram."""
        overview = get_workflow_overview()
        # Should have some kind of flow indicator
        assert "-->" in overview or "GATHER" in overview


class TestGetHandoffAdvice:
    """Tests for get_handoff_advice function."""

    def test_gemini_to_claude(self):
        """Test handoff advice from Gemini to Claude."""
        advice = get_handoff_advice("gemini", "claude")
        assert "Research Brief" in advice
        assert isinstance(advice, str)

    def test_claude_to_openai(self):
        """Test handoff advice from Claude to OpenAI."""
        advice = get_handoff_advice("claude", "openai")
        assert "Audit" in advice

    def test_claude_to_gemini(self):
        """Test handoff advice from Claude to Gemini."""
        advice = get_handoff_advice("claude", "gemini")
        assert "Research" in advice

    def test_openai_to_claude(self):
        """Test handoff advice from OpenAI to Claude."""
        advice = get_handoff_advice("openai", "claude")
        assert "Recommendations" in advice

    def test_case_insensitive(self):
        """Test handoff advice is case-insensitive."""
        advice1 = get_handoff_advice("GEMINI", "CLAUDE")
        advice2 = get_handoff_advice("gemini", "claude")
        assert advice1 == advice2

    def test_alias_codex(self):
        """Test codex alias works in handoff."""
        advice = get_handoff_advice("claude", "codex")
        assert isinstance(advice, str)
        # Should map to claude -> openai

    def test_alias_anthropic(self):
        """Test anthropic alias works in handoff."""
        advice = get_handoff_advice("anthropic", "gemini")
        assert isinstance(advice, str)
        # Should map to claude -> gemini

    def test_same_tool_handoff(self):
        """Test handoff to same tool."""
        advice = get_handoff_advice("claude", "claude")
        assert "No handoff needed" in advice

    def test_unknown_handoff(self):
        """Test handoff between unknown tools."""
        advice = get_handoff_advice("unknown1", "unknown2")
        assert "No specific handoff advice" in advice

    def test_gemini_to_openai_no_direct(self):
        """Test Gemini to OpenAI (no direct path defined)."""
        advice = get_handoff_advice("gemini", "openai")
        # This combination isn't in HANDOFF_ADVICE
        assert "No specific handoff advice" in advice


class TestGetWorkflowDiagram:
    """Tests for get_workflow_diagram function."""

    def test_returns_string(self):
        """Test diagram returns a string."""
        diagram = get_workflow_diagram()
        assert isinstance(diagram, str)

    def test_contains_boxes(self):
        """Test diagram contains ASCII boxes."""
        diagram = get_workflow_diagram()
        assert "+" in diagram
        assert "-" in diagram

    def test_contains_tool_names(self):
        """Test diagram contains tool names."""
        diagram = get_workflow_diagram()
        assert "GEMINI" in diagram
        assert "CLAUDE" in diagram
        assert "OPENAI" in diagram

    def test_contains_roles(self):
        """Test diagram contains role descriptions."""
        diagram = get_workflow_diagram()
        assert "Scout" in diagram or "Research" in diagram
        assert "Builder" in diagram or "Architect" in diagram
        assert "Auditor" in diagram

    def test_contains_arrows(self):
        """Test diagram contains flow arrows."""
        diagram = get_workflow_diagram()
        assert "-->" in diagram

    def test_contains_deliverables(self):
        """Test diagram contains deliverables."""
        diagram = get_workflow_diagram()
        assert "Brief" in diagram or "Research" in diagram
        assert "Code" in diagram
        assert "Recommendations" in diagram or "review" in diagram.lower()


class TestIntegration:
    """Integration tests for workflow module."""

    def test_full_workflow_flow(self):
        """Test complete workflow: get roles, handoff, diagram."""
        # Get all roles
        roles = get_all_roles()
        assert len(roles) == 3

        # Get handoff advice for typical flow
        advice1 = get_handoff_advice("gemini", "claude")
        advice2 = get_handoff_advice("claude", "openai")
        assert advice1 != advice2

        # Get overview and diagram
        overview = get_workflow_overview()
        diagram = get_workflow_diagram()
        assert overview != diagram  # They should be different content

    def test_role_deliverables_match_handoff(self):
        """Test that role deliverables align with handoff advice."""
        gemini = get_role_info("gemini")
        advice = get_handoff_advice("gemini", "claude")

        # Gemini's deliverable should be mentioned in handoff
        # Both mention "Research Brief"
        assert "Research" in gemini.deliverable or "Brief" in gemini.deliverable
