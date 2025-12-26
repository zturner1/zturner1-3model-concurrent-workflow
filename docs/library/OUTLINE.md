# CLI Tool: Deep Dive & Best Practices

## Overview
- Purpose and scope
- What the tool is and who it is for
- High-level capabilities

## 1. CLI Usage & Arguments
- Invocation modes
- Common flags
- Input/output patterns

### Basic Commands
- Interactive mode
- One-shot query
- Resume or continue sessions
- Pipe input into context

### Advanced Flags
- Output control
- Debugging/logging
- Prompt configuration
- Safety/permission controls

## 2. Slash Commands
- Environment controls
- Context management
- Tooling and diagnostics

| Command | Description |
| :--- | :--- |
| `/init` | |
| `/help` | |
| `/clear` | |
| `/compact` | |
| `/cost` | |
| `/model` | |
| `/permissions` | |
| `/bug` | |
| `/doctor` | |
| `/context` | |
| `/memory` | |
| `/mcp` | |
| `/review` | |
| `/pr-comments` | |
| `/sandbox` | |
| `/exit` | |

## 3. Configuration & Context
- Core config file(s)
- Location and lifecycle
- What to store vs. avoid
- Best practices for maintainability

## 4. Best Practices for "Best Use"

### A. Context Management
- Keep context lean
- Summarize when switching topics
- Use external sources appropriately

### B. Workflow Patterns
1. TDD workflow
2. Reviewer workflow
3. Incremental refactoring workflow

### C. Automation & Scripting
- Custom commands
- CI/CD usage

## 5. Integration in a Multi-Model System
- Research role
- Reasoning role
- Execution role
