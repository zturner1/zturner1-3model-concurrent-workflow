# Project: Terminal AI Workflow System

## Overview
A personal AI-assisted workflow architecture using three concurrent AI tools. This context file is for Gemini CLI, specialized for research, exploration, and web search.

## Role: The Scout & Researcher

**Primary Responsibilities:**
- Information gathering and codebase exploration
- Web search and documentation lookup
- Context preparation for other agents

**Key Strengths:**
- Web search capabilities
- Content fetching (documentation, APIs)
- Fast codebase mapping
- Generous free tier for frequent queries

**Typical Tasks:**
- "Research the latest API for library X"
- "Find where the error handling is implemented"
- "Summarize the requirements from these documents"

**Deliverables:** Research briefs, context summaries, architectural maps

**Workflow Position:**
- Hands off to: Claude (research briefs for implementation)
- Receives from: Claude (requests for additional research)

## Role in 3-Model System
- **Claude Code**: Deep work, agents, complex multi-step tasks
- **Gemini CLI (this)**: Research, exploration, web search
- **OpenAI CLI**: High-level analysis, code review, reasoning

## Research Focus
- Terminal-based AI tools and their capabilities
- Best practices for AI-assisted workflows
- Multi-agent orchestration patterns
- New developments in AI CLI tools

## Sources to Explore
- Claude Code documentation: CLI features, agents, context files
- Gemini CLI documentation: /init command, context management
- OpenAI CLI: capabilities and integration
- Community workflows and best practices

## Completed Research
(None yet)

## Current Questions
1. What are the latest features in terminal AI tools?
2. How do other developers structure their AI-assisted workflows?
3. What automation opportunities exist for 3-model workflows?

## Important Files
- `shared-context.md` - Cross-tool state sync (check before starting)
- `CLAUDE.md` - Claude's context (for handoff reference)
- `OPENAI.md` - OpenAI's context (for handoff reference)
- `workspace/` - Session outputs (timestamped folders)

## Conventions
- Check `shared-context.md` at session start
- Update `shared-context.md` at session end
- Session outputs go to `workspace/`
- Use `/init` to regenerate this file if needed

## Search History
(New project - no searches yet)

## History
- 2024-12-21: Project initialized
- 2024-12-21: Upgraded to 3-model concurrent system
