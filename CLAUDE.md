# Project: Terminal AI Workflow System

## Overview
A personal AI-assisted workflow architecture that makes AI work inside projects rather than in browser tabs. Context persists across sessions, multiple AI tools share state, and agents handle parallel tasks.

## Current Status
- **Active**: Initial setup complete
- **Blockers**: None
- **Next**: Test workflow with a real task

## Key Decisions
- 2024-12-21: Architecture designed with root-level context files (CLAUDE.md, GEMINI.md) for auto-loading
- 2024-12-21: Using .styles/ for output style definitions
- 2024-12-21: shared-context.md for cross-tool synchronization

## Important Files
- `architecture_layout.md` - Full architecture documentation
- `Knowledge.md` - Original vision/philosophy article
- `shared-context.md` - Cross-tool state sync
- `.styles/` - Output style definitions

## Conventions
- Context files in project root (auto-loaded by tools)
- Research outputs go to `research/summaries/`
- Drafts versioned as `title-v1.md`, `title-v2.md`
- Commit messages use `[type] description` format
- Update context at end of each session

## History
- 2024-12-21: Project initialized with full architecture setup
