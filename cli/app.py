"""Typer application for Terminal AI Workflow CLI."""

import typer
from typing import Optional
from pathlib import Path

from . import display
from .repl import run_repl
from .executor import get_tools_status
from .config import get_config, reload_config

app = typer.Typer(
    name="workflow",
    help="Terminal AI Workflow - 3-model concurrent AI system",
    add_completion=False,
)


@app.command()
def main(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed routing info"),
    debug: bool = typer.Option(False, "--debug", "-d", help="Enable debug mode"),
    status: bool = typer.Option(False, "--status", "-s", help="Show tool status and exit"),
    version: bool = typer.Option(False, "--version", "-V", help="Show version and exit"),
):
    """
    Terminal AI Workflow CLI - Interactive REPL for multi-model AI.

    Routes your requests to Claude, Gemini, or OpenAI based on keywords.
    """
    if version:
        from . import __version__
        display.console.print(f"Terminal AI Workflow CLI v{__version__}")
        raise typer.Exit()

    if status:
        try:
            tools_status = get_tools_status()
            display.show_status(tools_status)
        except Exception as e:
            display.show_error(f"Could not load config: {e}")
        raise typer.Exit()

    # Validate config exists
    config_path = Path("config/role_config.json")
    if not config_path.exists():
        display.show_error(f"Config file not found: {config_path}")
        display.console.print("[dim]Run from project root or check your installation.[/dim]")
        raise typer.Exit(1)

    # Run the REPL
    try:
        if debug:
            verbose = True
            display.show_info("Debug mode enabled")

        run_repl(verbose=verbose)
    except KeyboardInterrupt:
        display.console.print("\n[dim]Goodbye![/dim]")
    except Exception as e:
        display.show_error(str(e))
        raise typer.Exit(1)


def cli():
    """Entry point for the CLI."""
    app()


if __name__ == "__main__":
    cli()
