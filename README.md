# 🤖 3-Model Concurrent AI Workflow

<div align="center">

![Version](https://img.shields.io/badge/version-1.0-blue.svg)
![Status](https://img.shields.io/badge/status-untested-yellow.svg)
![License](https://img.shields.io/badge/license-CC%20BY--NC%204.0-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)

**Run Claude, Gemini, and OpenAI simultaneously on the same project.**

*Context persists. Files are truth. You own everything.*

[Quick Start](#-quick-start) • [Architecture](#-architecture) • [Documentation](#-documentation) • [Contributing](#-contributing)

</div>

---

## 🎯 The Problem

Browser-based AI workflows are **broken**:

- 😫 Context breaks mid-conversation
- 📋 Copy-paste between tabs
- 🗂️ Work scattered across chats
- 🔒 Vendor lock-in

## ✨ The Solution

Terminal-based AI that lives **inside** your project:

- 🚀 **3 AI tools running concurrently** — each with its specialty
- 💾 **Persistent context files** — survive sessions, travel with your project
- 📁 **Shared directories** — all tools contribute to the same outputs
- 🔓 **You own everything** — Git versioned, portable, provider-agnostic

---

## 🏗️ Architecture

```
┌────────────────────────────────────────────────────────────┐
│                      PROJECT FOLDER                        │
├────────────────────────────────────────────────────────────┤
│                                                            │
│   ┌──────────┐   ┌──────────┐   ┌──────────┐               │
│   │ CLAUDE.md│   │GEMINI.md │   │OPENAI.md │ Context Files │
│   └────┬─────┘   └────┬─────┘   └────┬─────┘               │
│        │              │              │                     │
│        └──────────────┼──────────────┘                     │
│                       ▼                                    │
│           ┌────────────────────┐                           │
│           │ shared-context.md  │                Sync Layer │
│           └────────────────────┘                           │
│                       │                                    │
│        ┌──────────────┼──────────────┐                     │
│        ▼              ▼              ▼                     │
│   ┌─────────┐   ┌──────────┐   ┌──────────┐                │
│   │research/│   │ drafts/  │   │ output/  │  Shared Output │
│   └─────────┘   └──────────┘   └──────────┘                │
│                                                            │
└────────────────────────────────────────────────────────────┘
                            │
       ┌────────────────────┼────────────────────┐
       ▼                    ▼                    ▼
 ┌───────────┐       ┌───────────┐       ┌───────────┐
 │  Claude   │       │  Gemini   │       │  OpenAI   │
 │   Code    │       │   CLI     │       │   CLI     │
 ├───────────┤       ├───────────┤       ├───────────┤
 │ • Agents  │       │ • Web     │       │ • Code    │
 │ • Files   │       │   Search  │       │   Review  │
 │ • Complex │       │ • Research│       │ • Analysis│
 └───────────┘       └───────────┘       └───────────┘
```

---

## 🛠️ Tool Roles

| Tool | Role | Best For |
|:-----|:-----|:---------|
| 🟣 **Claude Code** | Deep Work | Agents, complex tasks, file operations |
| 🔵 **Gemini CLI** | Research | Web search, exploration, fact-finding |
| 🟢 **OpenAI CLI** | Analysis | Code review, reasoning, evaluation |

---

## 🚀 Quick Start

### Prerequisites

- 📦 [Node.js](https://nodejs.org) v18+
- 🔧 Git
- 🔑 Accounts: Anthropic, Google, OpenAI

### Installation

```bash
# Clone the repo
git clone https://github.com/zturner1/zturner1-3model-concurrent-workflow.git
cd zturner1-3model-concurrent-workflow

# Install all 3 CLI tools
install.bat
```

### Authentication

```bash
claude      # 🟣 Follow browser login
gemini      # 🔵 Authenticate with Google
# 🟢 Set OPENAI_API_KEY environment variable
```

### Launch

```bash
run.bat
```

```
========================================
 🤖 Terminal AI Workflow - 3 Model System
========================================

 [1] 🟣 Claude Code  - Deep work, agents
 [2] 🔵 Gemini CLI   - Research, web search
 [3] 🟢 OpenAI CLI   - Analysis, code review
 [4] 🚀 All Three    - Launch all concurrently
 [5] Exit
```

---

## 📁 Project Structure

```
project/
├── 🟣 CLAUDE.md           # Claude context (auto-loads)
├── 🔵 GEMINI.md           # Gemini context (auto-loads)
├── 🟢 OPENAI.md           # OpenAI context (auto-loads)
├── 🔄 shared-context.md   # Cross-tool sync
├── 🎨 .styles/            # Output style definitions
├── 📚 research/           # Research outputs
├── 📝 drafts/             # Work in progress
├── 📦 output/             # Final deliverables
├── ⚙️ scripts/            # Automation
└── 📖 docs/               # Documentation
```

---

## 📖 Documentation

| Doc | Description |
|:----|:------------|
| 📐 [Architecture](architecture_layout.md) | Complete system documentation |
| 💡 [Philosophy](docs/philosophy.md) | Why terminal AI changes everything |
| 📊 [Diagrams](docs/diagram.md) | Visual workflow diagrams |
| 📋 [Requirements](requirements.md) | Setup and prerequisites |

---

## 🔄 How It Works

1. **Context files persist** — Each tool reads its context on startup
2. **Shared sync** — `shared-context.md` keeps all tools aligned
3. **Parallel work** — Use each tool for what it does best
4. **File-based output** — All work goes to project directories
5. **Git versioning** — Full history of your project and context

---

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Ways to Help

- 🐛 Report bugs
- 💡 Suggest features
- 📝 Improve documentation
- 🔧 Add Linux/macOS scripts

---

## 📄 License

[CC BY-NC 4.0](LICENSE) — Free to use and modify, but **no commercial use without permission**.

---

<div align="center">

**Built for developers who want AI to work *with* their projects, not around them.**

⭐ Star this repo if you find it useful!

</div>
