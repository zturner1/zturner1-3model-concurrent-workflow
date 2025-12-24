# 3-Model Concurrent AI Workflow

<div align="center">

![Version](https://img.shields.io/badge/version-1.0-blue.svg)
![Status](https://img.shields.io/badge/status-beta-green.svg)
![License](https://img.shields.io/badge/license-CC%20BY--NC%204.0-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)

**Run Claude, Gemini, and OpenAI simultaneously on the same project.**

*Context persists. Files are truth. You own everything.*

[Quick Start](#quick-start) | [Architecture](#architecture) | [Documentation](#documentation) | [Contributing](#contributing)

</div>

---

## The Problem

Browser-based AI workflows are **broken**:

- Context breaks mid-conversation
- Copy-paste between tabs
- Work scattered across chats
- Vendor lock-in

## The Solution

Terminal-based AI that lives **inside** your project:

- **3 AI tools running concurrently** - each with its specialty
- **Persistent context files** - survive sessions, travel with your project
- **Shared directories** - all tools contribute to the same outputs
- **You own everything** - Git versioned, portable, provider-agnostic

---

## Architecture

```
project/
  CLAUDE.md           (Claude context)
  GEMINI.md           (Gemini context)
  OPENAI.md           (OpenAI context)
  shared-context.md   (cross-tool sync)
  workspace/          (session outputs)
```

---

## Tool Roles

| Tool | Role | Best For |
|:-----|:-----|:---------|
| **Claude Code** | Deep Work | Agents, complex tasks, file operations |
| **Gemini CLI** | Research | Web search, exploration, fact-finding |
| **OpenAI CLI** | Analysis | Code review, reasoning, evaluation |

---

## Feature Status

| Feature | Status | Notes |
|:--------|:------:|:------|
| **Core** | | |
| Interactive router | OK | Keyword-based task routing |
| GUI mode (`run_gui.bat`) | Planned | Separate windows (not included) |
| CLI mode (`run_cli.bat`) | OK | Sequential in single terminal |
| Smart task routing | OK | Routes by first word of sentence |
| Session workspaces | OK | Timestamped folders in `workspace/` |
| **Tools** | | |
| Claude Code integration | OK | Deep work, file operations |
| Gemini CLI integration | OK | Research, web search |
| OpenAI Codex integration | OK | Analysis, code review |
| **Configuration** | | |
| `.env` support | OK | API keys loaded automatically |
| `role_config.json` | OK | Customizable routing rules |
| Context files auto-load | OK | CLAUDE.md, GEMINI.md, OPENAI.md |
| **Logging & Debug** | | |
| Activity logging | OK | `logs/run.log` |
| Log rotation (100MB) | OK | Keeps 5 backup files |
| Debug mode | OK | `run_cli.bat --debug` |
| Validation script | OK | `scripts/test_setup.ps1` |
| **Collaboration** | | |
| Shared context sync | OK | `shared-context.md` |
| Agent collaboration context | OK | Agents know each other's tasks |
| **Planned** | | |
| `/workspace` command | Planned | Session management |
| Linux/macOS support | Planned | Currently Windows only |
| Custom routing rules UI | Planned | Edit rules via command |

---

## Quick Start

### Prerequisites

- [Node.js](https://nodejs.org) v18+
- Git
- Accounts: Anthropic, Google, OpenAI

### Installation

```bash
# Clone the repo
git clone https://github.com/zturner1/zturner1-3model-concurrent-workflow.git
cd zturner1-3model-concurrent-workflow

# Install all 3 CLI tools
scripts\install.bat
```

### Authentication

```bash
# Claude - Follow browser login
claude

# Gemini - Authenticate with Google
gemini

# OpenAI - Set API key (choose one method):
```

**Option A: Environment Variable (recommended)**
```bash
# Windows (current session)
set OPENAI_API_KEY=sk-your-key-here

# Windows (permanent) - Run as Administrator
setx OPENAI_API_KEY "sk-your-key-here"
```

**Option B: Use .env file**
```bash
# Copy the example file
copy .env.example .env

# Edit .env and add your key
notepad .env
```

> Get your OpenAI API key at: https://platform.openai.com/api-keys

### Launch

```bash
run_cli.bat    # Sequential mode (1 terminal)
```

```
========================================
 Terminal AI Workflow - 3 Model System
========================================

 Type your task(s) and press Enter.
 Multiple sentences are split and routed to appropriate tools.

 Commands: /help, /status, /tasks, /exit
========================================

> Research AI trends. Build a summary. Review the draft.

  ----------------------------------------
  Analyzing and Routing Tasks
  ----------------------------------------
    gemini -> Research AI trends
    claude -> Build a summary
    openai -> Review the draft

  ----------------------------------------
  Launching Tools
  ----------------------------------------
    Starting Claude Code...
    Starting Gemini CLI...
    Starting OpenAI Codex...
```

**Routing keywords:**
- `research, search, find, explore...` -> Gemini
- `review, analyze, evaluate, compare...` -> OpenAI
- `build, create, fix, implement...` -> Claude (default)

---

## Project Structure

```
project/
  CLAUDE.md           # Claude context (auto-loads)
  GEMINI.md           # Gemini context (auto-loads)
  OPENAI.md           # OpenAI context (auto-loads)
  shared-context.md   # Cross-tool sync
  .styles/            # Output style definitions
  docs/               # Documentation
    library/          # Reference docs (accessible via /docs)
  scripts/            # Automation & launchers
  cli/                # Python CLI module
  config/             # Runtime configuration
  logs/               # Execution logs
  workspace/          # Session outputs
```

---

## Documentation

| Doc | Description |
|:----|:------------|
| [Architecture](docs/architecture.md) | Complete system documentation |
| [Philosophy](docs/philosophy.md) | Why terminal AI changes everything |
| [Diagrams](docs/diagram.md) | Visual workflow diagrams |

---

## How It Works

1. **Context files persist** - Each tool reads its context on startup
2. **Shared sync** - `shared-context.md` keeps all tools aligned
3. **Parallel work** - Use each tool for what it does best
4. **File-based output** - All work goes to project directories
5. **Git versioning** - Full history of your project and context

---

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Ways to Help

- Report bugs
- Suggest features
- Improve documentation
- Add Linux/macOS scripts

---

## License

[CC BY-NC 4.0](LICENSE) - Free to use and modify, but **no commercial use without permission**.

---

<div align="center">

**Built for developers who want AI to work *with* their projects, not around them.**

Star this repo if you find it useful!

</div>
