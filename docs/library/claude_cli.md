# Claude Code CLI: Deep Dive & Best Practices

## Overview

Claude Code CLI (`claude`) is an advanced AI assistant designed to live in your terminal. It acts not just as a chatbot, but as an agentic pair programmer capable of editing files, running shell commands, and managing complex coding tasks.

**Target Audience:** Developers, System Architects, and "Power Users" who prefer terminal-centric workflows.

## 1. CLI Usage & Arguments
The CLI can be invoked in several modes.

### Basic Commands
*   **Interactive Mode:**
    ```bash
    claude
    ```
    Starts a persistent chat session.
*   **One-Shot Query:**
    ```bash
    claude "query"
    ```
    Runs a single request without entering a session.
*   **Resume Last Session:**
    ```bash
    claude -c
    # or
    claude --continue
    ```
    Resumes the last session.
*   **Resume Specific Session:**
    ```bash
    claude -r <id>
    # or
    claude --resume <id>
    ```
    Resumes a specific session by ID.
*   **Piped Input:**
    ```bash
    cat logs.txt | claude -p "Analyze"
    ```
    Pipes text into the context.

### Advanced Flags
*   `--print`: Prints the response to stdout (useful for piping output to other tools).
*   `--verbose`: Enables verbose logging for debugging.
*   `--system-prompt <text>`: Overrides the default system prompt.
*   `--system-prompt-file <path>`: Loads a system prompt from a file.
*   `--dangerously-skip-permissions`: Skips permission prompts (use with caution in CI/CD).

## 2. Slash Commands
Slash commands control the environment, context, and tool behavior.

| Command | Description |
| :--- | :--- |
| `/init` | Initializes a project, creating a `CLAUDE.md` context file. |
| `/help` | Lists available commands. |
| `/clear` | Clears the immediate conversation history (but keeps project context). |
| `/compact` | Summarizes and compacts the conversation history to save tokens. |
| `/cost` | Displays current session cost and token usage. |
| `/model` | Switch models (e.g., Claude 3.5 Sonnet, Claude 3 Opus). |
| `/permissions` | View and modify tool execution permissions. |
| `/bug` | Report a bug to Anthropic. |
| `/doctor` | Checks installation health. |
| `/context` | Visualizes the current context window usage. |
| `/memory` | Edits the `CLAUDE.md` file directly. |
| `/mcp` | Manage Multi-Context Provider (MCP) servers. |
| `/review` | Requests a code review of current changes. |
| `/pr-comments` | Fetches and displays comments from a linked Pull Request. |
| `/sandbox` | Enables/disables sandboxed execution for safety. |
| `/exit` | Exits the session. |

## 3. Configuration & Context
Configuration and context are captured in local files that persist across sessions.

### Primary Config File
*   **File**: `CLAUDE.md`.
*   **Location**: Project root (`./CLAUDE.md`) or global (`~/.claude/CLAUDE.md`).
*   **Role**: Stores architectural patterns, coding standards, build instructions, and common commands.
*   **Best Practice**: Keep it concise. Use it to "onboard" Claude to your specific codebase conventions.

### Supporting Files
*   *None noted in this document.*

### Authentication
*   *Not covered in this document.*

## 4. Best Practices for "Best Use"

### A. Context Management
*   **Don't dump everything**: Use `@file` referencing selectively.
*   **Use `/compact` often**: Long sessions degrade performance and increase cost. Compact or `/clear` when changing topics.
*   **Leverage MCP**: Connect to database schemas or external docs via MCP instead of pasting them.

### B. Workflow Patterns
1.  **TDD (Test-Driven Development)**:
    *   **Scenario:** Implementing a new feature with unclear edge cases.
    *   **Action:** Ask for tests first, then implement to pass them.
    *   **Command:** `claude -p "Write tests for X, then propose the minimal code to pass them."`
2.  **The "Reviewer" Role**:
    *   **Scenario:** Reviewing a set of changes before a commit.
    *   **Action:** Pipe the diff for a bug-focused review.
    *   **Command:** `git diff | claude -p "Review these changes for bugs"`
3.  **Complex Refactoring**:
    *   **Scenario:** Refactoring a large or tightly coupled module.
    *   **Action:** Split into analysis, plan, and execution steps.
    *   **Command:** `claude -p "Analyze dependencies for X, propose a plan, then execute step 1."`

### C. Automation & Scripting
*   **Custom Commands**: Create markdown files in `.claude/commands/` to define custom slash commands (e.g., `/deploy` that runs a specific script).
*   **CI/CD**: Use `claude --print` in scripts to generate commit messages or changelogs automatically.

## 5. Integration in 3-Model System
*   **Gemini (Research)**: Finds libraries, reads docs, summarizes architectural patterns.
*   **OpenAI (Reasoning)**: Reviews complex logic, validates the architectural approach.
*   **Claude (Execution)**: Takes the research and plan, implements the code, runs the tests, and manages the file edits.
