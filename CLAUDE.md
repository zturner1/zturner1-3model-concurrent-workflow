# Project: Terminal AI Workflow System

## Overview
A personal AI-assisted workflow architecture using three concurrent AI tools. This context file is for Claude Code, specialized for deep work, agents, and complex multi-step tasks.

## Role in 3-Model System
- **Claude Code (this)**: Deep work, agents, complex multi-step tasks
- **Gemini CLI**: Research, exploration, web search
- **OpenAI CLI**: High-level analysis, code review, reasoning

## Current Status
- **Active**: 3-model architecture setup complete
- **Blockers**: None
- **Next**: Test concurrent workflow with all three tools

## Key Decisions
- 2024-12-21: Architecture designed with root-level context files for auto-loading
- 2024-12-21: Using .styles/ for output style definitions
- 2024-12-21: shared-context.md for cross-tool synchronization
- 2024-12-21: Upgraded to 3-model concurrent architecture (Claude, Gemini, OpenAI)

## Important Files
- `architecture_layout.md` - Full architecture documentation
- `Knowledge.md` - Original vision/philosophy article
- `shared-context.md` - Cross-tool state sync (check before starting)
- `GEMINI.md` - Gemini's context (for handoff reference)
- `OPENAI.md` - OpenAI's context (for handoff reference)
- `.styles/` - Output style definitions

## Conventions
- Check `shared-context.md` at session start
- Update `shared-context.md` at session end
- Context files in project root (auto-loaded by tools)
- Research outputs go to `research/summaries/`
- Drafts versioned as `title-v1.md`, `title-v2.md`
- Commit messages use `[type] description` format

## Claude-Specific Capabilities
- Spawn agents for parallel subtasks
- Extended context window
- Direct file read/write operations
- Complex multi-step task execution

## History
- 2024-12-21: Project initialized with full architecture setup
- 2024-12-21: Upgraded to 3-model concurrent system
