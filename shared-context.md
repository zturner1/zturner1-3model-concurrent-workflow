# Shared Project Context

Last updated: 2025-12-22
Updated by: Claude Code

## 3-Model Architecture

| Tool | Role | Context File |
|------|------|--------------|
| Claude Code | Deep work, agents, complex tasks | CLAUDE.md |
| Gemini CLI | Research, exploration, web search | GEMINI.md |
| OpenAI CLI | High-level analysis, code review | OPENAI.md |

## Project State
- **Phase**: Implementation Complete
- **Priority**: Production testing
- **Deadline**: None

## Active Tasks
1. Test full workflow with real tasks
2. Monitor for bugs/issues

## Recent Changes
- 2024-12-21 (Claude): Initial project setup
- 2024-12-21 (Claude): Upgraded to 3-model concurrent architecture
- 2025-12-22 (Claude): Major implementation session:
  - Merged run.bat and router.bat into unified interactive router
  - Added .env support for API keys
  - Fixed routing bugs (BOM encoding, batch script parsing)
  - Added collaboration context for agents (shared workspace)
  - Added session workspaces with manifests
  - Added window arrangement (side-by-side)
  - Implemented CLI mode (/cli flag)
  - Added logging with 100MB rotation
  - Created launcher scripts for each tool

## Features Implemented
- **GUI Mode**: Concurrent execution in separate windows
- **CLI Mode**: Sequential execution in single terminal (`run.bat /cli`)
- **Smart Routing**: Keywords route to appropriate tools
- **Collaboration**: Agents share workspace and know each other's tasks
- **Logging**: All activity logged to `logs/run.log`

## Handoff Notes
System is ready for production testing. Next session:
- Run full end-to-end test with all 3 tools
- Monitor for any issues
- Consider adding `/workspace` command for session management

## Sync Protocol
1. **Start session**: Read this file first
2. **During work**: Note any major changes
3. **End session**: Update "Recent Changes" and "Handoff Notes"
4. **Switch tools**: Add explicit handoff context
