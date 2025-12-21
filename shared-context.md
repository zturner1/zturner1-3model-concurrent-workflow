# Shared Project Context

Last updated: 2024-12-21
Updated by: Claude Code

## 3-Model Architecture

| Tool | Role | Context File |
|------|------|--------------|
| Claude Code | Deep work, agents, complex tasks | CLAUDE.md |
| Gemini CLI | Research, exploration, web search | GEMINI.md |
| OpenAI CLI | High-level analysis, code review | OPENAI.md |

## Project State
- **Phase**: Setup Complete
- **Priority**: Test 3-model concurrent workflow
- **Deadline**: None

## Active Tasks
1. Install all three CLI tools (run install.bat)
2. Authenticate each tool
3. Test concurrent workflow with run.bat option [4]

## Recent Changes
- 2024-12-21 (Claude): Initial project setup
- 2024-12-21 (Claude): Upgraded to 3-model concurrent architecture
- 2024-12-21 (Claude): Added OPENAI.md, updated all context files

## Handoff Notes
All three context files are ready. Each tool knows its role:
- Claude: Use for complex tasks, spawning agents, file operations
- Gemini: Use for research, web searches, exploration
- OpenAI: Use for analysis, code review, high-level reasoning

Update this file when switching between tools to maintain sync.

## Sync Protocol
1. **Start session**: Read this file first
2. **During work**: Note any major changes
3. **End session**: Update "Recent Changes" and "Handoff Notes"
4. **Switch tools**: Add explicit handoff context
