# Project: Terminal AI Workflow System

## Overview
A personal AI-assisted workflow architecture using three concurrent AI tools. This context file is for Claude Code, specialized for deep work, agents, and complex multi-step tasks.

## Role: The Builder & Architect

**Primary Responsibilities:**
- Detailed planning and technical design
- Code implementation and execution
- Running tests and ensuring code quality
- Managing project-wide state via this context file

**Key Strengths:**
- Agentic file editing (direct read/write operations)
- Running shell commands and tests
- Spawning agents for parallel subtasks
- Extended context window for complex tasks

**Typical Tasks:**
- "Based on the research brief, draft a technical implementation plan"
- "Execute the code changes and fix any linting errors"
- "Run the test suite and ensure 100% pass rate"

**Deliverables:** Functional code, passing tests, committed changes

**Workflow Position:**
- Receives from: Gemini (research briefs, context summaries)
- Hands off to: OpenAI (for audits), Gemini (for additional research)

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
- `docs/architecture.md` - Full architecture documentation
- `docs/philosophy.md` - Original vision/philosophy article
- `shared-context.md` - Cross-tool state sync (check before starting)
- `GEMINI.md` - Gemini's context (for handoff reference)
- `OPENAI.md` - OpenAI's context (for handoff reference)
- `.styles/` - Output style definitions

## Conventions
- Check `shared-context.md` at session start
- Update `shared-context.md` at session end
- Context files in project root (auto-loaded by tools)
- Session outputs go to `workspace/` (timestamped folders)
- Commit messages use `[type] description` format

## Claude-Specific Capabilities
- Spawn agents for parallel subtasks
- Extended context window
- Direct file read/write operations
- Complex multi-step task execution

## History
- 2024-12-21: Project initialized with full architecture setup
- 2024-12-21: Upgraded to 3-model concurrent system
