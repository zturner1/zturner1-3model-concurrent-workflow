# AI CLI Command Reference

This cheat sheet summarizes common CLI commands for Google Gemini CLI, OpenAI Codex CLI, and Anthropic Claude Code. It aims to match the latest available references; the Codex section is based on the local guide in this folder.

---

## 1. Gemini CLI (google-gemini/gemini-cli)

### Start and prompt
- `gemini` Start interactive mode
- `echo "What is fine tuning?" | gemini` Non-interactive via pipe
- `gemini -p "What is fine tuning?"` or `gemini --prompt "..."` One-shot prompt

### Built-in slash commands (interactive)
- `/help` or `/?` Help
- `/chat save <tag>` Save a conversation checkpoint
- `/chat resume <tag>` Resume a saved checkpoint
- `/chat list` List saved checkpoints
- `/chat delete <tag>` Delete a checkpoint
- `/chat share file.md|file.json` Export the current chat
- `/clear` Clear screen (Ctrl+L)
- `/compress` Summarize and replace the chat context
- `/copy` Copy last output to clipboard
- `/directory add <path1>,<path2>` Add workspace directories
- `/directory show` Show added directories
- `/editor` Select editor
- `/extensions` List active extensions
- `/mcp` Show MCP servers and tools
- `/memory add <text>` Add to memory (GEMINI.md)
- `/memory show|refresh|list` Inspect or reload memory
- `/restore [tool_call_id]` Restore last checkpoint (if enabled)
- `/settings` Open settings editor
- `/stats` Session statistics
- `/theme` Choose theme
- `/auth` Change auth method
- `/about` Version info
- `/tools [desc|nodesc]` List tools
- `/privacy` Privacy notice
- `/vim` Toggle vim mode
- `/init` Generate GEMINI.md
- `/quit` or `/exit` Exit

### At commands and shell
- `@path/to/file` or `@path/to/dir` Inject file or directory contents into the prompt
- `!<shell_command>` Run a shell command
- `!` Toggle shell mode

Notes:
- `GEMINI.md` provides hierarchical memory.
- `.geminiignore` can exclude files from tool access.
- In shell mode, the subprocess sees `GEMINI_CLI=1`.

---

## 2. OpenAI Codex CLI (from local guide)

### Install
- `npm install -g @openai/codex`
- `brew install --cask codex`
- Prebuilt binary: download from GitHub releases, add to PATH, rename to `codex`

### Authenticate
- ChatGPT login: run `codex` and sign in via browser
- API key: `export OPENAI_API_KEY="sk-..."`

### Config
- File: `~/.codex/config.toml`
- Common options:
  - `model = "gpt-5-codex"`
  - `sandbox_mode = "workspace-write"`
  - `approval_mode = "auto"`
  - `preferred_auth_method = "chatgpt"` or `"apikey"`

### Common usage
- `codex` Interactive mode
- `codex "Explain this function"` One-shot prompt
- `codex exec --full-auto "Fix lint errors"` Non-interactive automation

### Useful flags (from guide)
- `--full-auto`
- `--sandbox danger-full-access`
- `--model gpt-5-codex`
- `--json`

---

## 3. Claude Code CLI (Anthropic)

### Commands
- `claude` Start interactive REPL
- `claude "query"` Start REPL with initial prompt
- `claude -p "query"` Print mode (SDK), then exit
- `cat file | claude -p "query"` Process piped input
- `claude -c` Continue most recent conversation
- `claude -c -p "query"` Continue via SDK
- `claude -r "<session>" "query"` Resume session by ID or name
- `claude update` Update to latest version
- `claude mcp` Configure MCP servers

### Flags (selected, see source for full list)
- `--add-dir <paths>` Add working directories
- `--agent <name>` Choose an agent for the session
- `--agents '<json>'` Define subagents via JSON
- `--allowedTools "<tools...>"` Tools allowed without prompts
- `--append-system-prompt "text"` Append to default system prompt
- `--betas <headers>` Add beta headers (API key users only)
- `--chrome` Enable Chrome integration
- `--continue`, `-c` Resume most recent conversation
- `--dangerously-skip-permissions` Skip permission prompts
- `--debug "filters"` Debug logging categories
- `--disallowedTools "<tools...>"` Remove tools from context
- `--enable-lsp-logging` LSP logs to `~/.claude/debug/`
- `--fallback-model <model>` Fallback model (print mode)
- `--fork-session` New session ID when resuming
- `--ide` Auto-connect to IDE
- `--include-partial-messages` Include streaming partials (print + stream-json)
- `--input-format text|stream-json` Input format (print mode)
- `--json-schema '<schema>'` Structured JSON output (print mode)
- `--max-turns <n>` Limit agentic turns
- `--mcp-config <paths|json>` Load MCP config
- `--model <alias|full>` Model alias or full name
- `--no-chrome` Disable Chrome integration
- `--output-format text|json|stream-json` Output format (print mode)
- `--permission-mode <mode>` Start in a permission mode
- `--permission-prompt-tool <tool>` MCP tool for permission prompts
- `--plugin-dir <dir>` Load plugins from a directory
- `--print`, `-p` Print mode (non-interactive)
- `--resume`, `-r` Resume session or open picker
- `--session-id <uuid>` Force session ID
- `--setting-sources user,project,local` Choose settings sources
- `--settings <file|json>` Load settings
- `--strict-mcp-config` Only use MCP config from `--mcp-config`
- `--system-prompt "text"` Replace system prompt
- `--system-prompt-file <file>` Replace system prompt from file (print mode)
- `--tools "Bash,Edit,Read"` Limit available tools
- `--verbose` Verbose logging
- `--version`, `-v` Print version

---

## Sources

- Gemini CLI docs: https://google-gemini.github.io/gemini-cli/docs/cli/
- Gemini CLI commands: https://google-gemini.github.io/gemini-cli/docs/cli/commands.html
- OpenAI Codex CLI guide (local): OpenAI_Codex_CLI_Guide.docx
- Claude Code CLI reference: https://code.claude.com/docs/en/cli-reference.md

---

## 4. Workflow Strategy

### The 3-Model Architecture
To maximize efficiency, assign specific roles to each AI agent:

1.  **Gemini (The Scout & Researcher)**
    *   **Role**: Information retrieval, codebase mapping, documentation search.
    *   **Tasks**:
        *   "Find the API documentation for X."
        *   "Where is the user authentication logic defined in this repo?"
        *   "Summarize the error logs."
    *   **Output**: Research briefs, architectural maps, todo lists.

2.  **Claude (The Builder & Architect)**
    *   **Role**: Planning, implementation, execution.
    *   **Tasks**:
        *   "Take this research brief and create a technical plan."
        *   "Implement the login feature."
        *   "Refactor the database schema."
    *   **Output**: Code changes, git commits, passed tests.

3.  **OpenAI (The Auditor)**
    *   **Role**: High-level reasoning, logic checks, "Second Opinion".
    *   **Usage**: Keep in reserve. Use when Claude is stuck or for critical systems.
    *   **Tasks**:
        *   "Audit this architectural plan for security flaws."
        *   "Optimize this O(n^2) algorithm."
        *   "Why is this race condition happening?"

