# Project: Terminal AI Workflow System

## Overview
A personal AI-assisted workflow architecture using three concurrent AI tools. This context file is for OpenAI CLI (Codex), specialized for high-level analysis and code review.

## Role in 3-Model System
- **Claude Code**: Deep work, agents, complex multi-step tasks
- **Gemini CLI**: Research, exploration, web search
- **OpenAI CLI (this)**: High-level analysis, code review, reasoning

## Current Status
- **Active**: Initial setup complete
- **Blockers**: None
- **Next**: Test 3-model concurrent workflow

## Key Decisions
- 2024-12-21: Adopted 3-model concurrent architecture
- 2024-12-21: OpenAI designated for analysis and code review tasks

## Important Files
- `architecture_layout.md` - Full architecture documentation
- `Knowledge.md` - Original vision/philosophy article
- `shared-context.md` - Cross-tool state sync (check before starting)
- `CLAUDE.md` - Claude's context (for handoff reference)
- `GEMINI.md` - Gemini's context (for handoff reference)

## Conventions
- Check `shared-context.md` at session start
- Update `shared-context.md` at session end
- Write analysis outputs to `research/summaries/`
- Write code reviews to `drafts/feedback/`

## Analysis Focus Areas
- Code architecture review
- Logic validation
- Trade-off analysis
- High-level planning

## History
- 2024-12-21: Added to 3-model concurrent system
