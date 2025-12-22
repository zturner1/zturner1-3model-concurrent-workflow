# Claude Code CLI: Deep Dive & Best Practices

## Overview
Claude Code CLI (`claude`) is an advanced AI assistant designed to live in your terminal. It acts not just as a chatbot, but as an agentic pair programmer capable of editing files, running shell commands, and managing complex coding tasks.

## 1. CLI Usage & Arguments
The CLI can be invoked in several modes.

### Basic Commands
*   `claude`: Starts an interactive REPL session.
*   `claude "query"`: Starts a session with an immediate query.
*   `claude -c` / `claude --continue`: Resumes the last session.
*   `claude -r <id>` / `claude --resume <id>`: Resumes a specific session.
*   `claude -p "text"`: Pipes text into the context (e.g., `cat logs.txt | claude -p "Analyze"`).

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

## 3. Configuration & Context (`CLAUDE.md`)
The `CLAUDE.md` file is the brain of your project. It persists across sessions.
*   **Location**: Project root (`./CLAUDE.md`) or global (`~/.claude/CLAUDE.md`).
*   **Purpose**: Stores architectural patterns, coding standards, build instructions, and common commands.
*   **Best Practice**: Keep it concise. Use it to "onboard" Claude to your specific codebase conventions.

## 4. Best Practices for "Best Use"

### A. Context Management
*   **Don't dump everything**: Use `@file` referencing selectively.
*   **Use `/compact` often**: Long sessions degrade performance and increase cost. Compact or `/clear` when changing topics.
*   **Leverage MCP**: Connect to database schemas or external docs via MCP instead of pasting them.

### B. Workflow Patterns
1.  **TDD (Test Driven Development)**:
    *   Ask Claude to write the *test* first.
    *   Run the test (it fails).
    *   Ask Claude to write the code to pass the test.
    *   This prevents "hallucinated" code that looks right but doesn't work.

2.  **The "Reviewer" Role**:
    *   Pipe `git diff` into Claude: `git diff | claude -p "Review these changes for bugs"`
    *   Use `/review` before committing complex changes.

3.  **Complex Refactoring**:
    *   Don't do it in one turn.
    *   Step 1: "Analyze the dependency chain of X."
    *   Step 2: "Propose a refactor plan."
    *   Step 3: "Execute step 1 of the plan."

### C. Automation & Scripting
*   **Custom Commands**: Create markdown files in `.claude/commands/` to define custom slash commands (e.g., `/deploy` that runs a specific script).
*   **CI/CD**: Use `claude --print` in scripts to generate commit messages or changelogs automatically.

## 5. Integration in 3-Model System
*   **Gemini (Research)**: Finds libraries, reads docs, summarizes architectural patterns.
*   **OpenAI (Reasoning)**: Reviews complex logic, validates the architectural approach.
*   **Claude (Execution)**: Takes the research and plan, implements the code, runs the tests, and manages the file edits.
