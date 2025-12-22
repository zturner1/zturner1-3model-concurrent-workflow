# Configuration

Runtime configuration for the Terminal AI Workflow system.

## Files

- `role_config.json` - Task routing rules and tool definitions
- `knowledge_index.json` - Cached document index (auto-generated)
- `tasks/` - Session task files for tool coordination

## role_config.json

Defines routing keywords and tool configuration:
- `roles` - Keyword-to-tool mapping (research, analysis, deep_work)
- `tools` - Tool definitions (claude, gemini, openai)
- `auth_status` - Tool availability flags

## tasks/

Session-specific files for multi-tool coordination:
- `_input.txt` - User input buffer
- `_active.txt` - Active tools for current session
- `_workspace.txt` - Current workspace path
- `{tool}.txt` - Assigned tasks per tool
