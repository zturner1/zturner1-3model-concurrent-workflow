#!/usr/bin/env python3
"""
Terminal AI Workflow CLI - Entry Point

Usage:
    python run_cli.py          # Start interactive REPL
    python run_cli.py --help   # Show help
    python run_cli.py --status # Check tool availability
"""

from cli.app import cli

if __name__ == "__main__":
    cli()
