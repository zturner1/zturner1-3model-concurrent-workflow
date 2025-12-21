# 3-Model Concurrent AI Workflow

Run Claude, Gemini, and OpenAI simultaneously on the same project. Context persists across sessions. Your files are the source of truth.

## The Problem

Browser-based AI workflows scatter your work across chats, tabs, and documents. Context breaks. Projects fragment. You lose control.

## The Solution

Terminal-based AI that lives **inside** your project folder:

- **3 AI tools running concurrently**, each with its specialty
- **Persistent context files** that survive sessions
- **Shared output directories** so all tools contribute to the same project
- **You own everything** — version with Git, back up, switch providers anytime

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        PROJECT FOLDER                            │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────┐    ┌──────────┐    ┌──────────┐                  │
│  │ CLAUDE.md│    │GEMINI.md │    │OPENAI.md │   Context Files  │
│  └────┬─────┘    └────┬─────┘    └────┬─────┘                  │
│       │               │               │                         │
│       ▼               ▼               ▼                         │
│  ┌─────────────────────────────────────────┐                   │
│  │          shared-context.md              │   Sync Layer      │
│  └─────────────────────────────────────────┘                   │
│       ┌───────────────┼───────────────┐                        │
│       ▼               ▼               ▼                         │
│  ┌─────────┐    ┌──────────┐    ┌──────────┐                   │
│  │research/│    │ drafts/  │    │ output/  │   Shared Output   │
│  └─────────┘    └──────────┘    └──────────┘                   │
└─────────────────────────────────────────────────────────────────┘
        │                     │                     │
        ▼                     ▼                     ▼
  ┌───────────┐        ┌───────────┐        ┌───────────┐
  │  Claude   │        │  Gemini   │        │  OpenAI   │
  │   Code    │        │   CLI     │        │   CLI     │
  ├───────────┤        ├───────────┤        ├───────────┤
  │ • Agents  │        │ • Web     │        │ • Code    │
  │ • Files   │        │   Search  │        │   Review  │
  │ • Complex │        │ • Research│        │ • Analysis│
  └───────────┘        └───────────┘        └───────────┘
```

## Quick Start

### Prerequisites

- [Node.js](https://nodejs.org) v18+
- Git
- Accounts: Anthropic, Google, OpenAI

### Install

```bash
# Clone the repo
git clone https://github.com/zturner1/zturner1-3model-concurrent-workflow.git
cd zturner1-3model-concurrent-workflow

# Install all 3 CLI tools
install.bat
```

### Authenticate

```bash
claude      # Follow browser login
gemini      # Authenticate with Google
# Set OPENAI_API_KEY environment variable
```

### Run

```bash
run.bat

# Select:
# [1] Claude Code  - Deep work, agents
# [2] Gemini CLI   - Research, web search
# [3] OpenAI CLI   - Analysis, code review
# [4] All Three    - Launch all concurrently
```

## Tool Roles

| Tool | Primary Use | Strengths |
|------|-------------|-----------|
| **Claude Code** | Complex tasks, agents | Extended context, multi-agent, file operations |
| **Gemini CLI** | Research, exploration | Web search, generous free tier |
| **OpenAI CLI** | Analysis, code review | Strong reasoning, code understanding |

## Project Structure

```
project/
├── CLAUDE.md              # Claude context (auto-loads)
├── GEMINI.md              # Gemini context (auto-loads)
├── OPENAI.md              # OpenAI context (auto-loads)
├── shared-context.md      # Cross-tool sync
├── .styles/               # Output style definitions
├── research/              # Research outputs
├── drafts/                # Work in progress
├── output/                # Final deliverables
├── scripts/               # Automation
└── docs/                  # Documentation
```

## Documentation

- [Full Architecture](architecture_layout.md) — Complete system documentation
- [Philosophy](docs/philosophy.md) — Why terminal AI changes everything
- [Workflow Diagrams](docs/diagram.md) — Visual system architecture
- [Requirements](requirements.md) — Setup and prerequisites

## How It Works

1. **Context files persist** — Each tool reads its context file on startup
2. **Shared sync** — `shared-context.md` keeps all tools aligned
3. **Parallel work** — Use each tool for what it does best
4. **File-based output** — All work goes to project directories
5. **Git versioning** — Full history of your project and context

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

[CC BY-NC 4.0](LICENSE) - Free to use and modify, but **no commercial use without permission**.
