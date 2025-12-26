#!/usr/bin/env python3
"""
Terminal AI Workflow CLI - Entry Point

Usage:
    python run_cli.py          # Start interactive REPL
    python run_cli.py --help   # Show help
    python run_cli.py --status # Check tool availability
"""

import sys
from pathlib import Path

# Add parent directory to path so 'cli' package can be found
sys.path.insert(0, str(Path(__file__).parent.parent))

from cli.app import cli

if __name__ == "__main__":
    cli()
