# Requirements

## 3-Model Concurrent Architecture

This project uses three AI tools running simultaneously, each with specific strengths:

| Tool | Primary Use | Strengths |
|------|-------------|-----------|
| Claude Code | Deep work, agents, complex tasks | Extended context, multi-agent, file ops |
| Gemini CLI | Research, exploration | Web search, generous free tier |
| OpenAI CLI | High-level analysis, code review | Strong reasoning, code understanding |

## Terminal AI Tools

### Claude Code
- **Install**: `npm install -g @anthropic-ai/claude-code`
- **Auth**: Run `claude` and follow browser OAuth login
- **Context**: Reads `CLAUDE.md` from project root
- **Docs**: https://docs.anthropic.com/claude-code

### Gemini CLI
- **Install**: `npm install -g @google/gemini-cli`
- **Auth**: Run `gemini` and authenticate with Google account
- **Context**: Reads `GEMINI.md` from project root (use `/init` to create)
- **Docs**: https://ai.google.dev/gemini-cli

### OpenAI CLI (Codex)
- **Install**: `npm install -g @openai/codex`
- **Auth**: Set environment variable `OPENAI_API_KEY=your-key`
- **Context**: Reads `OPENAI.md` from project root
- **Docs**: https://platform.openai.com/docs

## Prerequisites

### Required
- **Node.js** (v18+): https://nodejs.org
- **Git**: https://git-scm.com
- **npm**: Comes with Node.js

### Optional
- **Windows Terminal**: Better terminal experience (multiple tabs)
- **VS Code**: For editing files

## API Keys / Accounts

| Tool | Account Required | Your Status |
|------|------------------|-------------|
| Claude Code | Anthropic account | Paid |
| Gemini CLI | Google account | Paid |
| OpenAI CLI | OpenAI account + API key | Paid (ChatGPT Plus) |

**Note**: ChatGPT Plus and OpenAI API are separate. You may need to add API credits at https://platform.openai.com/account/billing

## Quick Check

Run these to verify installation:
```bash
node --version    # Should be v18+
npm --version     # Should be v9+
git --version     # Any recent version
claude --version  # After install
gemini --version  # After install
codex --version   # After install
```

## Environment Variables

For OpenAI CLI, set your API key:

**Windows (temporary)**:
```cmd
set OPENAI_API_KEY=sk-your-key-here
```

**Windows (permanent)**:
1. Search "Environment Variables" in Start
2. Add new User variable: `OPENAI_API_KEY` = `sk-your-key-here`

## Quick Start

1. Run `install.bat` to install all three tools
2. Authenticate each tool (see instructions above)
3. Run `run.bat` to launch your workflow
4. Enter a multi-sentence task (e.g., "Research X. Build Y. Review Z.") to route to appropriate tools
