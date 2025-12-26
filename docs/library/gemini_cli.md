# Gemini CLI: Deep Dive & Best Practices

## Overview

The Gemini CLI (`google-gemini/gemini-cli`) is a versatile, terminal-based interface for Google's Gemini models. In the context of our **Terminal AI Workflow System**, it serves as the **Scout & Researcher**. Its primary strength lies in its ability to quickly ingest context, perform web searches (if enabled/available via tools), and generate architectural maps or research briefs without the overhead of heavy implementation tools.

**Target Audience:** Developers, System Architects, and "Power Users" who prefer terminal-centric workflows.

## 1. CLI Usage & Arguments

The CLI supports multiple invocation modes suited for different workflow stages.

### Basic Commands

*   **Interactive Mode:**
    ```bash
    gemini
    ```
    Starts a persistent chat session. Best for iterative research and exploration.

*   **One-Shot Query:**
    ```bash
    gemini -p "What is the latest version of React?"
    # or
    gemini --prompt "Explain this error"
    ```
    Ideal for quick lookups without entering a session.

*   **Piped Input:**
    ```bash
    cat error.log | gemini
    # or
    echo "Refactor this JSON" | gemini
    ```
    Feeds standard input into the context. Useful for debugging logs or processing file contents.

### Advanced Flags
*   **Shell Mode (`!`)**: Execute shell commands directly from the prompt (e.g., `!ls -la`).
*   **Context Injection (`@`)**: Directly reference files or directories in your prompt:
    *   `@src/main.rs`: Adds file content.
    *   `@docs/`: Adds directory tree and content (subject to token limits).

## 2. Slash Commands

Gemini CLI uses slash commands to manage the environment and session.

| Command | Description |
| :--- | :--- |
| `/init` | Generates a `GEMINI.md` context file in the current directory. |
| `/help` | Displays the help menu and list of available commands. |
| `/clear` | Clears the terminal screen (Ctrl+L). |
| `/chat` | Manage sessions: `save`, `resume`, `list`, `delete`, `share`. |
| `/directory` | Manage workspace directories: `add`, `show`. |
| `/memory` | Manage `GEMINI.md` memory: `add`, `show`, `refresh`, `list`. |
| `/mcp` | Inspect Model Context Protocol (MCP) servers and tools. |
| `/settings` | Open the settings editor (JSON configuration). |
| `/stats` | Show session statistics (token usage, etc.). |
| `/tools` | List available tools (with or without descriptions). |
| `/exit` | Exit the CLI session. |

*Note: Some standard commands from other CLIs (like `/doctor` or `/cost`) are handled via `/stats` or external setup.*

## 3. Configuration & Context

Configuration and context are captured in local files that persist across sessions.

### Primary Config File
*   **File**: `GEMINI.md`.
*   **Location:**
    *   **Global:** `~/.gemini/GEMINI.md` (User preferences, cross-project facts).
    *   **Project:** `./GEMINI.md` (Project role, specific architectural constraints).
*   **Role**: Core memory file that grounds responses.
*   **Lifecycle**: Created via `/init`. Updated manually or via `/memory add`.
*   **Best Practice**: Keep the project `GEMINI.md` focused on *high-level* architecture and current objectives. Don't dump entire codebases here.

### Supporting Files
*   **File**: `.geminiignore`.
*   **Role**: Prevents the CLI from reading specific files or directories (e.g., `node_modules`, `.env`, `dist`), ensuring context remains clean and secure.

### Authentication
*   *Not covered in this document.*

## 4. Best Practices for "Best Use"

### A. Context Management
*   **The "Scout" Mindset:** As the researcher, your goal is *breadth* and *mapping*. Use `@path/to/dir` to list files and understand structure, but only read specific files when necessary.
*   **Hierarchical Memory:** Use Global memory for *who you are* (the user) and Project memory for *what you are doing*.
*   **Refresh Often:** Use `/memory refresh` if you edit `GEMINI.md` externally during a session.

### B. Workflow Patterns
1.  **The Research Brief:**
    *   **Scenario:** A user asks, "How do I implement X?"
    *   **Action:** Search docs, check existing code, and produce a concise brief.
    *   **Command:** `gemini -p "Create a research brief for implementing X."`
2.  **The Error Investigator:**
    *   **Scenario:** An error log needs triage.
    *   **Action:** Pipe logs and ask for the source.
    *   **Command:** `cat error.log | gemini -p "Locate the source of this error."`
3.  **Context Prepper:**
    *   **Scenario:** Preparing for a large refactor.
    *   **Action:** Summarize module architecture to a temporary brief.
    *   **Command:** `gemini -p "Summarize the architecture of @src/module into a brief."`

### C. Automation & Scripting
*   **Pipe Chains:** combine Gemini with other tools.
    *   `git diff | gemini "Write a commit message" > commit_msg.txt`

## 5. Integration in a Multi-Model System

In the **3-Model Architecture**:

*   **Role:** **The Scout & Researcher**
*   **Responsibility:**
    *   **Input:** Vague requests ("I want to add auth"), error logs, new documentation URLs.
    *   **Action:** Explore the codebase, fetch web content, summarize findings.
    *   **Output:** Concrete, actionable "Research Briefs" or "Context Maps" for **Claude** (The Builder).
*   **Handoff:**
    *   Do not attempt complex code generation if it requires multi-file coordination (that is Claude's job).
    *   *Do* provide the exact file paths and snippets Claude will need.
