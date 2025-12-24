# OpenAI CLI: Deep Dive & Strategy

## Overview
The OpenAI CLI serves as the **Auditor and High-Level Reasoner** in the 3-model system. While Gemini scouts and Claude builds, the OpenAI CLI provides a "second opinion," performs complex logic checks, and validates architectural decisions. It is optimized for pure reasoning tasks rather than file manipulation.

## 1. Installation & Configuration
*(Based on local guides)*

*   **Install**: `npm install -g @openai/codex` (or similar wrapper)
*   **Auth**: `export OPENAI_API_KEY="sk-..."`
*   **Config**: `~/.codex/config.toml` or `OPENAI.md` in the project root.

## 2. Core Usage

### Modes
*   **Interactive**: Run `codex` (or the alias configured) for a chat session.
*   **One-Shot**: `codex "Explain this logic"`
*   **Automation**: `codex exec --full-auto "Refactor this file"` (Use with caution).

### Key Flags
*   `--model`: Select the specific reasoning model (e.g., `gpt-4o`, `o1-preview`).
*   `--json`: Force JSON output (useful for piping to other tools).
*   `--temperature 0`: Use for deterministic logic/code analysis.

## 3. The "Auditor" Workflows

### A. The Architecture Review
**Goal**: Validate a plan created by Claude before writing code.
1.  **Input**: Paste the plan or pipe `cat plan.md`.
2.  **Prompt**: "Act as a Senior Principal Engineer. Critique this plan for scalability bottlenecks and security flaws."
3.  **Result**: A list of risks.
4.  **Action**: Update the plan, then hand back to Claude.

### B. The Logic Puzzle
**Goal**: Solve a complex algorithm that is causing bugs.
1.  **Input**: The specific function causing trouble.
2.  **Prompt**: "This function has a race condition. Trace the execution flow and identify the exact moment it desynchronizes."
3.  **Result**: A step-by-step logic trace.

### C. The Code Reviewer
**Goal**: Review changes before a commit.
1.  **Pipe**: `git diff --staged | codex "Review these changes"`
2.  **Focus**: Ask for specific feedback: "Are there any unhandled edge cases?"

## 4. Integration with `OPENAI.md`
*   **Purpose**: Stores "Principles" and "Reasoning Rules."
*   **Content**:
    *   "Always prefer composition over inheritance."
    *   "Security: Input must always be sanitized."
*   **Effect**: The CLI prepends these rules to every request, ensuring consistent "personality" and standards.

## 5. Best Practices
*   **Keep it Pure**: Avoid using OpenAI for heavy file editing or web searching (use Claude/Gemini). Use it for *thinking*.
*   **Prompt Engineering**: OpenAI models often respond best to "Persona" prompting (e.g., "You are a security expert...").
*   **Verify**: Use the CLI to verify specific tricky snippets of code that Claude generated.
