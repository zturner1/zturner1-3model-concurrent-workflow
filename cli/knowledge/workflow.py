"""Workflow strategy access for Document Library knowledge."""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List

# Path to the workflow strategy document
WORKFLOW_STRATEGY_PATH = Path("docs/library/Workflow_Strategy.md")


@dataclass
class RoleInfo:
    """Information about a tool's role in the workflow."""
    tool_id: str
    name: str
    role_title: str
    description: str
    key_strengths: List[str]
    typical_tasks: List[str]
    deliverable: str
    usage_note: Optional[str] = None


# Hardcoded role definitions based on Workflow_Strategy.md
ROLES = {
    "gemini": RoleInfo(
        tool_id="gemini",
        name="Gemini CLI",
        role_title="The Scout & Researcher",
        description="Information gathering, codebase exploration, and context preparation.",
        key_strengths=[
            "Web search",
            "Content/documentation fetching",
            "Fast codebase mapping"
        ],
        typical_tasks=[
            "Research the latest API for library X",
            "Find where the error handling is implemented",
            "Summarize the requirements from documents"
        ],
        deliverable="Research Brief or Context Summary"
    ),
    "claude": RoleInfo(
        tool_id="claude",
        name="Claude Code",
        role_title="The Builder & Architect",
        description="Detailed planning, code implementation, and execution.",
        key_strengths=[
            "Agentic file editing",
            "Running shell commands/tests",
            "Managing project-wide state (via CLAUDE.md)"
        ],
        typical_tasks=[
            "Draft a technical implementation plan",
            "Execute code changes and fix linting errors",
            "Run the test suite and ensure 100% pass rate"
        ],
        deliverable="Functional code, passing tests, committed changes"
    ),
    "openai": RoleInfo(
        tool_id="openai",
        name="OpenAI Codex",
        role_title="The Auditor",
        description="High-level reasoning, logic validation, and fallback support.",
        key_strengths=[
            "Pure logic reasoning (o1/gpt-4o models)",
            "Complex algorithmic optimization",
            "Fresh eyes auditing"
        ],
        typical_tasks=[
            "Audit Claude's plan for security issues",
            "Solve algorithmic bottlenecks",
            "Provide second opinion when stuck"
        ],
        deliverable="Logic corrections, architectural critiques, optimized algorithms",
        usage_note="Reserve. Not a daily driver; use to avoid friction."
    )
}


# Handoff advice between tools
HANDOFF_ADVICE = {
    ("gemini", "claude"): (
        "Gemini hands off to Claude with a **Research Brief**:\n"
        "- Summary of findings\n"
        "- Relevant code locations\n"
        "- Recommended next steps\n\n"
        "Claude receives context and begins implementation planning."
    ),
    ("claude", "openai"): (
        "Claude hands off to OpenAI for **Audit**:\n"
        "- Share the implementation plan or code\n"
        "- Ask specific questions about logic/security\n"
        "- Request optimization suggestions\n\n"
        "OpenAI provides critique and returns to Claude."
    ),
    ("claude", "gemini"): (
        "Claude hands off to Gemini for **Additional Research**:\n"
        "- Specific questions that need web search\n"
        "- Documentation lookup requests\n"
        "- Codebase exploration tasks\n\n"
        "Gemini returns findings to Claude."
    ),
    ("openai", "claude"): (
        "OpenAI hands off to Claude with **Recommendations**:\n"
        "- Logic corrections to apply\n"
        "- Architectural suggestions\n"
        "- Optimizations to implement\n\n"
        "Claude applies changes and continues work."
    )
}


def get_role_info(tool: str) -> Optional[RoleInfo]:
    """Get role information for a specific tool.

    Args:
        tool: One of 'claude', 'gemini', 'openai'

    Returns:
        RoleInfo object or None if not found
    """
    tool_lower = tool.lower()

    # Handle aliases
    if tool_lower in ("codex", "gpt"):
        tool_lower = "openai"
    elif tool_lower in ("anthropic",):
        tool_lower = "claude"
    elif tool_lower in ("google",):
        tool_lower = "gemini"

    return ROLES.get(tool_lower)


def get_all_roles() -> List[RoleInfo]:
    """Get role information for all tools."""
    return list(ROLES.values())


def get_workflow_overview() -> str:
    """Get the complete workflow overview as formatted text."""
    return """# 3-Model Workflow Architecture

## Workflow Flow
```
GATHER (Gemini) --> PLAN & EXECUTE (Claude) --> AUDIT (OpenAI)
     |                      |                        |
     v                      v                        v
Research Brief         Working Code            Logic Corrections
```

## Role Summary

| Tool | Role | Primary Focus |
|------|------|---------------|
| **Gemini** | Scout & Researcher | Information gathering, exploration |
| **Claude** | Builder & Architect | Implementation, execution, testing |
| **OpenAI** | Auditor | Reasoning, validation, optimization |

## Usage Guidelines

1. **Start with Gemini** for research and exploration tasks
2. **Hand off to Claude** with a research brief for implementation
3. **Use OpenAI selectively** for audits and second opinions

## Task Distribution Reference
- Gemini: 35% (research, exploration)
- Claude: 40% (implementation, deep work)
- OpenAI: 25% (analysis, review) - *reserve capacity*
"""


def get_handoff_advice(from_tool: str, to_tool: str) -> str:
    """Get advice for handing off between two tools.

    Args:
        from_tool: Source tool ('claude', 'gemini', 'openai')
        to_tool: Target tool ('claude', 'gemini', 'openai')

    Returns:
        Handoff advice string
    """
    from_lower = from_tool.lower()
    to_lower = to_tool.lower()

    # Normalize tool names
    for original, normalized in [("codex", "openai"), ("gpt", "openai"),
                                  ("anthropic", "claude"), ("google", "gemini")]:
        if from_lower == original:
            from_lower = normalized
        if to_lower == original:
            to_lower = normalized

    key = (from_lower, to_lower)

    if key in HANDOFF_ADVICE:
        return HANDOFF_ADVICE[key]

    if from_lower == to_lower:
        return f"No handoff needed - continuing with {from_tool}."

    return f"No specific handoff advice for {from_tool} -> {to_tool}."


def get_workflow_diagram() -> str:
    """Get ASCII workflow diagram."""
    return """
    +------------------+     +----------------------+     +------------------+
    |    GEMINI        |     |       CLAUDE         |     |     OPENAI       |
    |  Scout/Research  | --> |  Builder/Architect   | --> |     Auditor      |
    +------------------+     +----------------------+     +------------------+
            |                         |                          |
            v                         v                          v
    +------------------+     +----------------------+     +------------------+
    | - Web search     |     | - Code implementation|     | - Logic review   |
    | - Documentation  |     | - File editing       |     | - Security audit |
    | - Exploration    |     | - Test execution     |     | - Optimization   |
    +------------------+     +----------------------+     +------------------+
            |                         |                          |
            v                         v                          v
      Research Brief           Working Code             Recommendations
"""
