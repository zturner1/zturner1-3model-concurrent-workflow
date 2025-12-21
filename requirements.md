# Requirements

## Terminal AI Tools

### Claude Code
- **Install**: `npm install -g @anthropic-ai/claude-code`
- **Auth**: Run `claude` and follow login prompts (uses browser OAuth)
- **Docs**: https://docs.anthropic.com/claude-code

### Gemini CLI
- **Install**: `npm install -g @anthropic-ai/claude-code` or via standalone installer
- **Auth**: Run `gemini` and authenticate with Google account
- **Docs**: https://ai.google.dev/gemini-cli

### Codex CLI (Optional)
- **Install**: `npm install -g @openai/codex`
- **Auth**: Requires OpenAI API key
- **Docs**: https://platform.openai.com

## Prerequisites

### Required
- **Node.js** (v18+): https://nodejs.org
- **Git**: https://git-scm.com
- **npm**: Comes with Node.js

### Optional
- **Windows Terminal**: Better terminal experience
- **VS Code**: For editing files

## API Keys / Accounts

| Tool | Account Required | Free Tier |
|------|------------------|-----------|
| Claude Code | Anthropic account | Limited |
| Gemini CLI | Google account | Generous |
| Codex CLI | OpenAI account + API key | Pay-per-use |

## Quick Check

Run these to verify installation:
```bash
node --version    # Should be v18+
npm --version     # Should be v9+
git --version     # Any recent version
claude --version  # After install
gemini --version  # After install
```
