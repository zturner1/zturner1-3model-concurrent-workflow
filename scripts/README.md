# Scripts

Launcher scripts and automation tools.

## Entry Points

- `run_cli.py` - Python CLI entry point (called by run_cli.bat)
- `install.bat` - Dependency installation script

## PowerShell Scripts

- `run_cli.ps1` - Sequential CLI executor
- `route_tasks.ps1` - Input parser and task router
- `test_setup.ps1` - Setup validation and health check

## tools/

Tool-specific launchers:
- `launch_claude.bat` - Claude Code launcher
- `launch_gemini.bat` - Gemini CLI launcher
- `launch_openai.bat` - OpenAI Codex launcher
- `arrange_windows.ps1` - Window arrangement utility

## Usage

From project root:
```bash
run_cli.bat           # Start interactive REPL
scripts\install.bat   # Install dependencies
```
