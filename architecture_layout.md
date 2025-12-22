# Personal AI Workflow Architecture

A comprehensive architecture for terminal-based AI-assisted workflows, enabling persistent context, multi-agent collaboration, and **3-model concurrent operation**.

---

## Philosophy

Traditional browser-based AI workflows fragment your work across chats, tabs, and documents. This architecture solves that by making AI work *inside* your projects:

- **File-based ownership**: Everything lives in files you control
- **Persistent context**: AI remembers your project across sessions
- **3-Model Concurrent**: Run Claude, Gemini, and OpenAI simultaneously
- **Tool-agnostic**: Switch between AI tools without losing state
- **Scalable**: From simple notes to complex multi-agent workflows

## 3-Model Architecture Overview

| Tool | Primary Role | Strengths |
|------|--------------|-----------|
| Claude Code | Deep work, agents, complex tasks | Extended context, multi-agent, file ops |
| Gemini CLI | Research, exploration | Web search, generous free tier |
| OpenAI CLI | High-level analysis, code review | Strong reasoning, code understanding |

All three tools operate on the same project folder, share context via `shared-context.md`, and write outputs to common directories.

---

## 1. Project Folder Structure

```
project/
├── CLAUDE.md                    # Claude Code context (auto-loads)
├── GEMINI.md                    # Gemini CLI context (auto-loads)
├── OPENAI.md                    # OpenAI CLI context (auto-loads)
├── shared-context.md            # Cross-tool sync (all 3 tools read this)
│
├── .styles/                     # Output style definitions
│   ├── research.md              # Research synthesis style
│   ├── technical.md             # Technical planning style
│   ├── review.md                # Critical review style
│   ├── script.md                # Script writing style
│   └── creative.md              # Creative writing style
│
├── research/                    # Research outputs from AI agents
│   ├── sources/                 # Collected references and citations
│   ├── summaries/               # Synthesized research summaries
│   └── raw/                     # Raw research dumps
│
├── drafts/                      # Work-in-progress documents
│   ├── v1/                      # First drafts
│   ├── v2/                      # Revisions
│   └── feedback/                # Agent critique and feedback
│
├── output/                      # Final deliverables
│   ├── published/               # Released/shared content
│   └── internal/                # Internal documentation
│
├── scripts/                     # Automation and utility scripts
│   ├── prompts/                 # Reusable prompt templates
│   └── tools/                   # Helper scripts
│
├── logs/                        # Session logs and decision history
│   └── decisions/               # Key decision records
│
└── archive/                     # Completed work for reference
    └── YYYY-MM/                 # Organized by date
```

### Directory Purposes

| Directory | Purpose | When to Use |
|-----------|---------|-------------|
| `CLAUDE.md` / `GEMINI.md` / `OPENAI.md` | AI memory (root level) | Auto-loaded by each tool on startup |
| `shared-context.md` | Cross-tool sync | Read at start, update at end of each session |
| `.styles/` | Output style definitions | Switch writing modes |
| `research/` | Information gathering | New topics, fact-finding, source collection |
| `drafts/` | Work in progress | Active writing and iteration |
| `output/` | Final deliverables | Completed, polished work |
| `scripts/` | Automation | Reusable prompts and helper tools |
| `logs/` | History | Session summaries, decision records |
| `archive/` | Reference | Completed projects, past work |

### Naming Conventions

- **Research files**: `topic-YYYY-MM-DD.md` (e.g., `ai-workflows-2024-01-15.md`)
- **Drafts**: `title-v1.md`, `title-v2.md` (version in filename)
- **Feedback**: `title-feedback-agent.md` (indicate source)
- **Decisions**: `YYYY-MM-DD-decision-topic.md`

### Cleanup Guidelines

- Move completed drafts to `output/` when finalized
- Archive projects monthly to `archive/YYYY-MM/`
- Clear `research/raw/` periodically (keep summaries)
- Review and prune context files when they grow large

---

## 2. Context File System

Context files are persistent memory for your AI tools. They load automatically when you start a session in the project folder.

### Initializing Context Files

**Gemini CLI:**
```bash
# In your project folder, run:
gemini

# Then use the /init command:
/init
```
This creates `GEMINI.md` with a basic project structure.

**Claude Code:**
```bash
# Simply create the file manually or ask Claude to create it:
claude

# Then say: "Create a CLAUDE.md context file for this project"
```

### Context Window Visibility

Terminal AI tools show your remaining context window, helping you manage long sessions:
- **Gemini CLI**: Displays remaining context in the terminal prompt
- **Claude Code**: Shows token usage and warns when approaching limits

This visibility helps you know when to:
- Summarize and compress context
- Start a fresh session
- Delegate to agents (which get fresh context windows)

### CLAUDE.md Template

```markdown
# Project: [Project Name]

## Overview
[Brief description of what this project is about and its goals]

## Current Status
- **Active**: [What you're currently working on]
- **Blockers**: [Any issues or questions]
- **Next**: [Planned next steps]

## Key Decisions
- [YYYY-MM-DD]: [Decision made and why]
- [YYYY-MM-DD]: [Another decision]

## Important Files
- `path/to/file.md` - [What this file contains]
- `path/to/another.md` - [Purpose of this file]

## Conventions
- [Project-specific rules, e.g., "Use APA citations"]
- [Style preferences, e.g., "Technical but accessible tone"]
- [Workflow rules, e.g., "Always get feedback before finalizing"]

## History
- [YYYY-MM-DD]: Started project with [initial goal]
- [YYYY-MM-DD]: Completed [milestone]
- [YYYY-MM-DD]: Changed direction to [new focus]
```

### GEMINI.md Template

```markdown
# Project: [Project Name]

## Role in 3-Model System
- Claude Code: Deep work, agents, complex tasks
- Gemini CLI (this): Research, exploration, web search
- OpenAI CLI: High-level analysis, code review

## Research Focus
[What topics need investigation]

## Sources to Explore
- [Topic 1]: [Specific questions]
- [Topic 2]: [What to look for]

## Completed Research
- `research/summaries/topic.md` - [Brief summary]

## Current Questions
1. [Open question needing research]
2. [Another question]

## Search History
- [YYYY-MM-DD]: Searched [topic], found [key insight]
```

### OPENAI.md Template

```markdown
# Project: [Project Name]

## Role in 3-Model System
- Claude Code: Deep work, agents, complex tasks
- Gemini CLI: Research, exploration, web search
- OpenAI CLI (this): High-level analysis, code review

## Analysis Focus
[What needs analysis or review]

## Pending Reviews
- `path/to/file` - [What to review]

## Completed Analysis
- `research/summaries/analysis.md` - [Brief summary]

## Code Review Queue
1. [File or feature to review]
2. [Another review task]

## Insights
- [YYYY-MM-DD]: [Key insight from analysis]
```

### shared-context.md Template (Cross-Tool Sync)

```markdown
# Shared Project Context

Last updated: [YYYY-MM-DD HH:MM]
Updated by: [Tool name]

## 3-Model Architecture

| Tool | Role | Context File |
|------|------|--------------|
| Claude Code | Deep work, agents, complex tasks | CLAUDE.md |
| Gemini CLI | Research, exploration, web search | GEMINI.md |
| OpenAI CLI | High-level analysis, code review | OPENAI.md |

## Project State
- **Phase**: [Planning/Research/Drafting/Review/Complete]
- **Priority**: [Current focus area]
- **Deadline**: [If applicable]

## Active Tasks
1. [Task being worked on]
2. [Next task]

## Recent Changes
- [YYYY-MM-DD]: [Change made by which tool]
- [YYYY-MM-DD]: [Another change]

## Handoff Notes
[Important context for the next tool/session]
```

### Context Management Best Practices

**Update Frequency:**
- Update context at the end of each session
- Add decisions immediately when made
- Update status when tasks complete

**Context Window Management:**
- Keep context files focused and concise
- Move historical details to `logs/`
- Summarize rather than accumulate

**When to Reset:**
- Project direction changes significantly
- Context becomes cluttered or contradictory
- Starting a new phase of work

---

## 3. Multi-Agent Workflow

Agents are specialized sub-AIs that handle specific tasks with fresh context windows, keeping your main conversation clean.

### Agent Types

| Agent Role | Purpose | Example Prompt |
|------------|---------|----------------|
| Research Agent | Gather information | "Research [topic]. Find 5 reputable sources. Write findings to `research/summaries/topic.md`" |
| Analysis Agent | Deep technical analysis | "Analyze [problem]. Consider trade-offs. Document in `drafts/analysis.md`" |
| Critique Agent | Review and feedback | "Review `drafts/article-v1.md`. Identify weaknesses. Write feedback to `drafts/feedback/`" |
| Writer Agent | Generate content | "Write [content type] based on `research/summaries/`. Save to `drafts/v1/`" |
| Planner Agent | Break down tasks | "Create implementation plan for [goal]. List steps in `logs/decisions/`" |

### Workflow Pattern

```
┌─────────────────────────────────────────────────────────┐
│                    Main Conversation                     │
│         (Strategic direction and oversight)              │
└───────────────┬───────────────────────────┬─────────────┘
                │                           │
                ▼                           ▼
    ┌───────────────────┐       ┌───────────────────┐
    │  Research Agent   │       │  Analysis Agent   │
    │  (Fresh context)  │       │  (Fresh context)  │
    └─────────┬─────────┘       └─────────┬─────────┘
              │                           │
              ▼                           ▼
    ┌───────────────────┐       ┌───────────────────┐
    │ research/topic.md │       │ drafts/analysis.md│
    └───────────────────┘       └───────────────────┘
                │                           │
                └───────────┬───────────────┘
                            ▼
              ┌─────────────────────────────┐
              │     Main: Synthesize        │
              │     Agent Outputs           │
              └─────────────────────────────┘
```

### Agent Guidelines

1. **Give focused prompts**: One clear task per agent
2. **Specify output location**: Tell agents where to write files
3. **Review before integrating**: Check agent output quality
4. **Chain strategically**: Use one agent's output as another's input

### Example Agent Prompts

**Research Agent:**
```
Research the current state of terminal-based AI tools (2024).
Focus on: Claude Code, Gemini CLI, and alternatives.
For each tool, document:
- Key features
- Pricing/availability
- Strengths and limitations
Write findings to research/summaries/terminal-ai-tools.md
Include sources with links.
```

**Critique Agent:**
```
Review drafts/article-v1.md with a critical eye.
Identify:
- Logical gaps or unsupported claims
- Areas needing more evidence
- Structural issues
- Unclear explanations
Write detailed feedback to drafts/feedback/article-v1-critique.md
Be constructive but thorough.
```

---

## 4. Output Styles

Output styles are predefined system prompts that shape how AI responds. Switch styles based on your current task.

### Style Definition Template

```markdown
# Style: [Name]

## Purpose
[When to use this style]

## Tone
[Formal/casual, technical/accessible, etc.]

## Structure
[Expected output format]

## Constraints
[Word limits, formatting rules, what to avoid]

## Example
[Sample output demonstrating this style]
```

### Default Styles

#### Research Synthesis (`.styles/research.md`)

```markdown
# Style: Research Synthesis

## Purpose
Compiling and summarizing research findings objectively.

## Tone
Academic, objective, evidence-based. Cite sources.

## Structure
1. Executive summary (2-3 sentences)
2. Key findings (bulleted)
3. Detailed analysis (by topic)
4. Sources (with links)
5. Open questions

## Constraints
- Always cite sources
- Present multiple perspectives
- Avoid personal opinions
- Use precise language
```

#### Technical Planning (`.styles/technical.md`)

```markdown
# Style: Technical Planning

## Purpose
Breaking down technical tasks into actionable steps.

## Tone
Precise, practical, implementation-focused.

## Structure
1. Goal statement
2. Prerequisites/dependencies
3. Step-by-step plan (numbered)
4. Potential challenges
5. Success criteria

## Constraints
- Concrete, specific steps
- Include time/effort indicators
- Note decision points
- Identify risks
```

#### Critical Review (`.styles/review.md`)

```markdown
# Style: Critical Review

## Purpose
Identifying weaknesses and areas for improvement.

## Tone
Constructive but thorough. Devil's advocate.

## Structure
1. Overall assessment
2. Strengths (brief)
3. Weaknesses (detailed)
4. Specific suggestions
5. Priority improvements

## Constraints
- Be specific, not vague
- Explain why something is weak
- Provide actionable fixes
- Balance criticism with constructive suggestions
```

#### Script Writing (`.styles/script.md`)

```markdown
# Style: Script Writing

## Purpose
Video scripts, tutorials, presentations, and spoken content.

## Tone
Conversational, clear, engaging. Written for the ear, not the eye.

## Structure
1. Hook (first 10 seconds)
2. Problem/context setup
3. Main content (chunked into segments)
4. Transitions between sections
5. Call to action / conclusion

## Constraints
- Short sentences (easy to speak)
- Active voice throughout
- Include timing notes [PAUSE], [EMPHASIS]
- Mark visual cues if needed: [SHOW: diagram]
- Avoid jargon unless explained
- Read aloud to test flow
```

#### Creative Writing (`.styles/creative.md`)

```markdown
# Style: Creative Writing

## Purpose
Engaging, narrative content creation.

## Tone
Dynamic, engaging, personality-driven.

## Structure
- Hook opening
- Natural flow
- Varied sentence structure
- Strong conclusion

## Constraints
- Show, don't tell
- Avoid clichés
- Match voice to audience
- Maintain consistent tone
```

### Switching Styles

In Claude Code, reference the style file in your prompt:
```
Using the style defined in .styles/research.md,
write a summary of the AI tools research.
```

---

## 5. Version Control Integration

Git enables tracking changes, collaboration, and recovery.

### Initial Setup

```bash
cd project/
git init
git add .
git commit -m "[meta] Initialize project structure"
```

### Commit Message Conventions

```
[type] Brief description

Types:
- [context] Context file updates
- [research] New research added
- [draft] Draft creation/revision
- [output] Final deliverable
- [meta] Project structure changes
- [style] Output style modifications
```

### Example Commits

```bash
git commit -m "[context] Update project status after research phase"
git commit -m "[research] Add terminal AI tools comparison"
git commit -m "[draft] Complete first draft of architecture article"
git commit -m "[output] Finalize and publish architecture guide"
```

### .gitignore

```gitignore
# Temporary files
*.tmp
*~
.DS_Store

# Large research dumps (optional - uncomment if needed)
# research/raw/*.pdf
# research/raw/*.epub

# Sensitive context (if any)
.private/

# Editor files
*.swp
.vscode/
.idea/
```

### Branch Strategy

- `main`: Stable, complete work
- `draft/[topic]`: Active drafting
- `research/[topic]`: Research exploration
- `experiment/[idea]`: Trying new approaches

### When to Commit

- End of each work session
- After significant decisions
- Before trying risky changes
- After completing milestones

---

## 6. Tool Interoperability (3-Model System)

Run all three AI tools concurrently, each handling its specialty.

### Tool Selection Guide

| Tool | Best For | Context File | Strengths |
|------|----------|--------------|-----------|
| Claude Code | Complex tasks, agents | CLAUDE.md | Extended context, multi-agent, file ops |
| Gemini CLI | Research, exploration | GEMINI.md | Web search, generous free tier |
| OpenAI CLI | Analysis, code review | OPENAI.md | Strong reasoning, code understanding |

### When to Use Each Tool

**Claude Code:**
- Multi-step complex tasks
- Spawning agents for parallel work
- File creation and editing
- Project-wide refactoring

**Gemini CLI:**
- Web research and fact-finding
- Exploring new topics
- Quick queries and exploration
- Compiling sources

**OpenAI CLI:**
- Code review and analysis
- Architecture evaluation
- Trade-off analysis
- High-level reasoning tasks

**Note:** Agents can use web search via different models, allowing you to leverage each tool's strengths for specific subtasks.

### Synchronization Protocol

```
Session Start:
1. Read shared-context.md
2. Note current project state
3. Load tool-specific context

During Session:
4. Update tool-specific context as needed
5. Write outputs to designated folders

Session End:
6. Update shared-context.md with changes
7. Add handoff notes for next session
8. Commit changes
```

### Handoff Example

When switching from Gemini (research) to Claude (writing):

**In shared-context.md:**
```markdown
## Handoff Notes
Completed research on terminal AI tools using Gemini.
Key findings in research/summaries/terminal-ai-tools.md
Ready for Claude to synthesize into article draft.
Focus areas: workflow benefits, context management.
```

### Conflict Resolution

- `shared-context.md` is the source of truth for cross-tool state
- Tool-specific contexts can have additional details
- When conflicts arise, check git history
- Add explicit notes when changing direction

---

## 7. Session Management

### Starting a Session

```bash
# Navigate to project
cd ~/projects/my-project

# Launch AI tool
claude
# or: gemini

# Context loads automatically from CLAUDE.md / GEMINI.md in root
```

**First actions in session:**
1. Review current status in context file
2. State your goal for this session
3. Check recent changes if continuing work

### During a Session

- Write outputs to appropriate folders
- Update context when making decisions
- Spawn agents for parallel/specialized work
- Note questions or blockers as they arise

### Ending a Session

**Checklist:**
1. [ ] Summarize what was accomplished
2. [ ] Update context file with:
   - Current status
   - Next steps
   - Any blockers or questions
3. [ ] Update shared-context.md if using multiple tools
4. [ ] Commit changes to git
5. [ ] Add handoff notes if pausing mid-task

### Session Summary Template

Add to context file at session end:
```markdown
## Session: YYYY-MM-DD

### Accomplished
- [What you completed]

### Next Steps
- [What to do next session]

### Notes
- [Any important observations or questions]
```

---

## 8. Backup and Recovery

### Backup Strategy

**Primary: Git**
- All project files versioned
- Remote repository (GitHub, GitLab) for off-machine backup
- Push regularly: `git push origin main`

**Critical Assets:**
- Context files (`CLAUDE.md`, `GEMINI.md`, `OPENAI.md`, `shared-context.md`)
- Research summaries (`research/summaries/`)
- Final outputs (`output/`)

### Recovery Scenarios

**Lost context file:**
1. Check git history: `git log --oneline CLAUDE.md`
2. Restore: `git checkout <commit> -- CLAUDE.md`
3. Or rebuild from output files and memory

**Corrupted project:**
1. Clone from remote: `git clone <repo-url>`
2. Check recent commits for issues
3. Reset if needed: `git reset --hard <safe-commit>`

**Fresh start needed:**
1. Archive current state: `mv project/ archive/project-YYYY-MM-DD/`
2. Create new project folder
3. Initialize fresh structure
4. Copy relevant outputs from archive

### Disaster Prevention

- Commit at least daily
- Push to remote at least weekly
- Don't store secrets in context files
- Keep sensitive info in `.private/` (gitignored)

---

## Quick Start Guide

### New Project Setup

```bash
# 1. Create project folder
mkdir my-project && cd my-project

# 2. Create structure
mkdir -p .styles research/{sources,summaries,raw} \
         drafts/{v1,v2,feedback} output/{published,internal} \
         scripts/{prompts,tools} logs/decisions archive .private

# 3. Create context files for all 3 tools
# (Or copy from a template project)

# 4. Initialize git
git init
echo "*.tmp" > .gitignore
echo ".private/" >> .gitignore
git add .
git commit -m "[meta] Initialize project"

# 5. Start working (all 3 tools)
run.bat
```

### 3-Model Daily Workflow

1. **Open terminal** in project folder
2. **Run `run.bat`** and enter a multi-sentence task to launch tools concurrently
3. **Check `shared-context.md`** - see current project state
4. **Assign tasks by tool strength:**
   - Claude: Complex tasks, agents, file edits
   - Gemini: Research, web search, exploration
   - OpenAI: Analysis, code review, reasoning
5. **Work in parallel** - each tool writes to project files
6. **Update `shared-context.md`** when switching focus
7. **Commit** - save your work with git

---

## Reference: File Templates

### Quick Context Template

```markdown
# Project: [Name]

## Now
[Current focus]

## Next
[Upcoming tasks]

## Decisions
- [Date]: [Decision]
```

### Research Note Template

```markdown
# Research: [Topic]
Date: YYYY-MM-DD

## Summary
[Key findings in 2-3 sentences]

## Details
[Detailed notes]

## Sources
- [Source 1](url)
- [Source 2](url)

## Questions
- [Open questions]
```

### Decision Record Template

```markdown
# Decision: [Title]
Date: YYYY-MM-DD

## Context
[Why this decision was needed]

## Options Considered
1. [Option A] - [Pros/Cons]
2. [Option B] - [Pros/Cons]

## Decision
[What was decided]

## Rationale
[Why this option was chosen]
```

---

*This architecture transforms AI from a chat interface into a collaborative 3-model workflow system. Your projects become the container — Claude, Gemini, and OpenAI become your team.*
