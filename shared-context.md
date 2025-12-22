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
- **Phase**: Beta Testing
- **Priority**: Production validation
- **Deadline**: None

## Active Tasks
1. Continue testing workflows
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
- 2025-12-22 (Claude): Cleanup & hardening:
  - Removed 12 .gitkeep files, .private/, requirements.md
  - Moved architecture_layout.md to docs/architecture.md
  - Added error handling for missing files in run.bat
  - Improved test_setup.ps1 with comprehensive validation
  - Added /debug mode for verbose logging
  - Added Feature Status table to README.md
  - Fixed launcher scripts working directory

## Features Implemented
- **GUI Mode**: Concurrent execution in separate windows (`run_gui.bat`)
- **CLI Mode**: Sequential execution in single terminal (`run_cli.bat`)
- **Debug Mode**: Verbose output (`run_gui.bat /debug`)
- **Smart Routing**: Keywords route to appropriate tools
- **Collaboration**: Agents share workspace and know each other's tasks
- **Logging**: All activity logged to `logs/run.log`
- **Validation**: Run `scripts/test_setup.ps1` to check setup

## Handoff Notes
System is in beta testing phase. All core features working.
- Error handling added for missing files
- Validation script improved
- Debug mode available for troubleshooting
- Feature status documented in README.md
- 2025-12-22: Major reorganization completed
  - Document_Library moved to docs/library/
  - Scripts consolidated into scripts/
  - README files added to all directories
  - Knowledge module integrated

## Sync Protocol
1. **Start session**: Read this file first
2. **During work**: Note any major changes
3. **End session**: Update "Recent Changes" and "Handoff Notes"
4. **Switch tools**: Add explicit handoff context

## Active Tasks
(None currently active)

