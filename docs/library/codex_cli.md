# OpenAI Codex CLI: Deep Dive & Best Practices

## Overview

The OpenAI Codex CLI (`@openai/codex`) serves as the **Auditor** in our **Terminal AI Workflow System**. Unlike the exploratory nature of Gemini or the builder focus of Claude, this tool is optimized for high-level reasoning, complex logic validation, and acting as a "Second Opinion" for critical architectural decisions.

**Target Audience:** Senior Engineers, Security Auditors, and developers needing robust logic verification.

## 1. CLI Usage & Arguments

The Codex CLI focuses on precise, programmable interactions rather than open-ended chat, though it supports both.

### Basic Commands

*   **Interactive Mode:**
    ```bash
    codex
    ```
    Starts the REPL environment. Useful for step-by-step logic debugging.

*   **One-Shot Query:**
    ```bash
    codex "Explain the time complexity of this function"
    ```
    Passes the query directly to the model and returns the result.

*   **Automation Mode:**
    ```bash
    codex exec --full-auto "Fix lint errors"
    ```
    Executes a task autonomously. *Note: Use with caution and appropriate sandbox settings.*

### Advanced Flags
*   `--model <model_name>`: Specify the model version (e.g., `gpt-5-codex`).
*   `--sandbox <level>`: Define the safety level (e.g., `danger-full-access`, `workspace-write`).
*   `--json`: Output responses in JSON format for parsing by other tools.
*   `--full-auto`: Authorization to proceed without user confirmation for each step (used in scripts).

## 2. Slash Commands

*Note: The Codex CLI relies more on configuration files and flags than the slash-command interface seen in Gemini or Claude. However, standard shell escapes are supported.*

| Command | Description |
| :--- | :--- |
| (none) | Codex CLI relies on flags and configuration instead of slash commands. |

*   **Shell Escape:**
    *   Use standard shell piping or the exec mode to interact with the system.
*   **Session Management:**
    *   Session persistence is often handled via the `config.toml` or specific state flags rather than manual `/save` commands.

## 3. Configuration & Context

Configuration and context are captured in local files for reproducible environments.

### Primary Config File
*   **File**: `config.toml`.
*   **Location**: `~/.codex/config.toml`.
*   **Role**: Centralized configuration for reproducible environments across the team.
*   **Key Settings:**
```toml
[general]
model = "gpt-5-codex"
approval_mode = "auto"       # Options: manual, auto
preferred_auth_method = "apikey" # Options: chatgpt, apikey

[sandbox]
mode = "workspace-write"     # Restricts file operations to the current workspace
```

### Supporting Files
*   *None noted in this document.*

### Authentication
*   **API Key:** `export OPENAI_API_KEY="sk-..."` (Recommended for CI/CD).
*   **Browser:** Run `codex` without a key to trigger the browser-based login flow.

## 4. Best Practices for "Best Use"

### A. Context Management
*   **The "Auditor" Mindset:** Do not overload the Auditor with the entire codebase. Provide only the *critical path* or the *specific module* in question.
*   **Sanitized Input:** When asking for a security review, ensure the input context is clean and focused to get the most accurate vulnerability assessment.

### B. Workflow Patterns
1.  **The Logic Check:**
    *   **Scenario:** Claude has proposed a complex algorithmic change.
    *   **Action:** Paste the algorithm and ask for edge cases and complexity.
    *   **Command:** `codex "Verify this algorithm for edge cases and O-notation complexity."`
2.  **The Security Audit:**
    *   **Scenario:** A new authentication flow is implemented.
    *   **Action:** Pipe the module for a security review.
    *   **Command:** `cat auth.ts | codex "Identify potential security flaws in this authentication logic."`
3.  **The "Second Opinion":**
    *   **Scenario:** You are stuck between two architectural patterns.
    *   **Action:** Provide requirements and ask for a trade-off analysis.
    *   **Command:** `codex "Compare these options and recommend one: A vs B."`

### C. Automation & Scripting
*   **CI/CD Integration:** Use `codex exec --full-auto` within a pipeline to run automated code reviews on Pull Requests.
*   **JSON Output:** Use `--json` to pipe the analysis results into a dashboard or a GitHub comment bot.

## 5. Integration in a Multi-Model System

In the **3-Model Architecture**:

*   **Role:** **The Auditor**
*   **Responsibility:**
    *   **Input:** Proposed code changes, complex algorithms, security-critical modules.
    *   **Action:** Deep reasoning, validation, verification.
    *   **Output:** Pass/Fail assessments, optimization suggestions, security warnings.
*   **Handoff:**
    *   **From Claude:** Claude finishes a task. You use Codex to verify the work before committing.
    *   **To Claude:** Codex finds a bug. You hand the bug report back to Claude for fixing.
    *   *Usage Rule:* Keep Codex in reserve. It is the heavy lifter for reasoning, not for scaffolding or exploration.
