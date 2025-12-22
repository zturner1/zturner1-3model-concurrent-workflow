# Workflow Strategy: 3-Model Architecture

This document outlines the strategic division of labor between Gemini, Claude, and OpenAI within our terminal-based AI workflow.

---

## 1. Gemini: The Scout & Researcher
**Primary Tool: `gemini`**

*   **Role**: Information gathering, codebase exploration, and context preparation.
*   **Key Strengths**: Web search, content fetching (documentation), and fast codebase mapping (`codebase_investigator`).
*   **Typical Tasks**:
    *   "Research the latest API for library X."
    *   "Find where the error handling for the auth module is implemented."
    *   "Summarize the requirements from these project documents."
*   **Deliverable**: A **Research Brief** or **Context Summary** to be handed off to the builder.

## 2. Claude: The Builder & Architect
**Primary Tool: `claude`**

*   **Role**: Detailed planning, code implementation, and execution.
*   **Key Strengths**: Agentic file editing, running shell commands/tests, and managing project-wide state (via `CLAUDE.md`).
*   **Typical Tasks**:
    *   "Based on the research brief, draft a technical implementation plan."
    *   "Execute the code changes and fix any linting errors."
    *   "Run the test suite and ensure 100% pass rate."
*   **Deliverable**: Functional code, passing tests, and committed changes.

## 3. OpenAI: The Auditor
**Primary Tool: `openai` / `codex`**

*   **Role**: High-level reasoning, logic validation, and fallback support.
*   **Status**: **Reserve.** Not a daily driver; used to avoid friction and maintain "clean" context.
*   **Key Strengths**: Pure logic reasoning (especially `o1`/`gpt-4o` models), complex algorithmic optimization, and "fresh eyes" auditing.
*   **Typical Tasks**:
    *   "Audit Claude's plan for potential security or concurrency issues."
    *   "Solve this specific algorithmic bottleneck."
    *   "Provide a second opinion if Claude gets stuck in a loop."
*   **Deliverable**: Logic corrections, architectural critiques, or optimized algorithms.

---

## Workflow Flowchart
1.  **GATHER** (Gemini) → 2.  **PLAN & EXECUTE** (Claude) → 3.  **AUDIT** (OpenAI - *Optional*)
