# Gemini CLI: Deep Dive & Workflow Guide

## Overview
The Gemini CLI (`gemini`) is your primary tool for **research, exploration, and context gathering**. In the 3-model architecture, it serves as the "Scout," rapidly traversing codebases, documentation, and web resources to prepare detailed briefings for other agents.

## 1. Installation & Setup
*(Based on project configuration)*

*   **Package**: `google-gemini/gemini-cli`
*   **Auth**: Requires a Google Cloud Project with the Vertex AI or Gemini API enabled.
    *   Run `gcloud auth login` or set `GOOGLE_APPLICATION_CREDENTIALS`.
*   **Initialization**: Run `/init` in a new project to generate `GEMINI.md`.

## 2. Core Commands & Usage

### Interactive Mode
*   `gemini`: Starts the conversational REPL.
*   `gemini "query"`: One-shot prompt (useful for quick answers).
*   `echo "text" | gemini`: Pipes input into the context.

### Essential Slash Commands
*   `/init`: Creates the `GEMINI.md` context file. **Always run this first.**
*   `/clear`: Resets the current conversation (saves tokens).
*   `/chat save <tag>`: Checkpoints a research session.
*   `/chat share`: Exports the chat to a file (great for handing off to Claude).
*   `/memory add <text>`: Saves a fact to `GEMINI.md` (long-term project memory).

## 3. The `GEMINI.md` Context File
Similar to `CLAUDE.md`, this file persists project-specific knowledge.
*   **Location**: Project root.
*   **Role**: Stores search history, key architectural facts found during research, and active "Open Questions."
*   **Workflow**:
    1.  Start a session.
    2.  Use `/memory add` to record findings.
    3.  The file updates, ensuring the next session "remembers" what you found.

## 4. Research Workflows (The "Scout" Role)

### A. The "Codebase Map"
**Goal**: Understand a new repository before changing it.
1.  **List**: `ls -R` or use `find` to see the structure.
2.  **Summarize**: "Summarize the purpose of the `src/utils` folder."
3.  **Document**: `/memory add "The utils folder contains A, B, and C."`

### B. The "Web Scavenger"
**Goal**: Find documentation for a library Claude needs to use.
1.  **Search**: "Search for the latest API reference for React 19 hooks."
2.  **Synthesize**: "Create a markdown summary of the new `use` hook."
3.  **Export**: Save the output to `docs/research/react_hooks.md`.
4.  **Handoff**: Tell Claude, "Read `docs/research/react_hooks.md` and implement..."

### C. Error Investigation
**Goal**: Root cause analysis.
1.  **Pipe**: `cat logs/error.log | gemini "Analyze this stack trace"`
2.  **Locate**: "Find the file and line number mentioned in the error."
3.  **Explain**: "Explain why this error might be happening given the code in `app.py`."

## 5. Tips for Success
*   **Be Specific**: Gemini excels at processing large amounts of text. Don't be afraid to pipe in whole files.
*   **Use Checkpoints**: Before going down a rabbit hole, use `/chat save exploration_start`.
*   **Clean Up**: Use `/clear` or `/compress` if the context gets too long/confusing.
