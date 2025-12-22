# CLI Module

Python CLI application for the Terminal AI Workflow system.

## Structure

```
cli/
├── __init__.py      # Package version and exports
├── app.py           # Typer CLI application entry point
├── config.py        # Configuration loader (.env + JSON)
├── display.py       # Rich console output formatting
├── executor.py      # Tool execution engine
├── repl.py          # Interactive REPL loop
├── router.py        # Task routing logic
└── knowledge/       # Document Library integration
    ├── index.py     # Document indexing and search
    ├── commands.py  # CLI command reference parser
    └── workflow.py  # Workflow strategy access
```

## Usage

Run via the root launcher:
```bash
run_cli.bat
```

Or directly with Python:
```bash
python scripts/run_cli.py
```

## REPL Commands

- `/help` - Show help
- `/status` - Check tool availability
- `/docs` - Browse Document Library
- `/ref` - CLI command reference
- `/workflow` - 3-model workflow guide
