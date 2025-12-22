"""Rich display utilities for Terminal AI Workflow CLI."""

from typing import List, Optional, Generator
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table
from rich.live import Live
from rich.spinner import Spinner
from rich.text import Text

from .router import Route

# Global console instance
console = Console()


def show_header():
    """Display the CLI header."""
    console.print(Panel.fit(
        "[bold blue]Terminal AI Workflow[/bold blue]\n"
        "[dim]Type /help for commands, /exit to quit[/dim]",
        border_style="blue"
    ))
    console.print()


def show_routing(routes: List[Route], verbose: bool = False):
    """Display routing information."""
    if not verbose:
        return

    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Tool", style="green")
    table.add_column("Task")

    for route in routes:
        table.add_row(route.tool_display_name, route.task[:50] + "..." if len(route.task) > 50 else route.task)

    console.print(table)
    console.print()


def show_tool_header(tool_name: str):
    """Display a header for tool output."""
    console.print(f"\n[bold cyan]─── {tool_name} ───[/bold cyan]")


def show_tool_footer():
    """Display a footer after tool output."""
    console.print("[dim cyan]───────────────────[/dim cyan]\n")


def stream_output(output_generator: Generator[str, None, None], tool_name: str):
    """Stream output with live markdown rendering."""
    buffer = ""

    show_tool_header(tool_name)

    try:
        with Live(Markdown(""), console=console, refresh_per_second=10, vertical_overflow="visible") as live:
            for chunk in output_generator:
                buffer += chunk
                # Update the live display with rendered markdown
                live.update(Markdown(buffer))
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted[/yellow]")

    show_tool_footer()
    return buffer


def show_output(text: str, tool_name: str):
    """Display static output with markdown rendering."""
    show_tool_header(tool_name)
    console.print(Markdown(text))
    show_tool_footer()


def show_spinner(message: str):
    """Create a spinner context manager."""
    return console.status(f"[bold blue]{message}[/bold blue]", spinner="dots")


def show_error(message: str):
    """Display an error message."""
    console.print(f"[bold red]Error:[/bold red] {message}")


def show_success(message: str):
    """Display a success message."""
    console.print(f"[bold green]Success:[/bold green] {message}")


def show_info(message: str):
    """Display an info message."""
    console.print(f"[bold blue]Info:[/bold blue] {message}")


def show_help():
    """Display help information."""
    help_text = """
## Commands

| Command | Description |
|---------|-------------|
| `/help` | Show this help message |
| `/status` | Check tool availability |
| `/tasks` | Show current task files |
| `/log` | Show recent log entries |
| `/clear` | Clear the screen |
| `/exit` | Exit the CLI |

## Documentation Commands

| Command | Description |
|---------|-------------|
| `/docs` | Browse Document Library |
| `/docs <name>` | View specific document |
| `/docs search <query>` | Search all documents |
| `/ref` | CLI command reference overview |
| `/ref <tool>` | Commands for claude/gemini/openai |
| `/workflow` | 3-model workflow overview |
| `/workflow roles` | Detailed role descriptions |

## Routing Keywords

| Keywords | Routes To |
|----------|-----------|
| `research`, `find`, `search`, `explore` | Gemini CLI |
| `analyze`, `review`, `audit`, `validate` | OpenAI Codex |
| `build`, `create`, `implement`, `fix`... | Claude Code (default) |

## Examples

```
> hello
> research what is markdown
> find the API documentation
> build a hello world script. review the code.
```
"""
    console.print(Markdown(help_text))


def show_status(tools_status: dict):
    """Display tool availability status."""
    table = Table(title="Tool Status", show_header=True, header_style="bold cyan")
    table.add_column("Tool", style="bold")
    table.add_column("Command")
    table.add_column("Status")

    for tool, info in tools_status.items():
        status = "[green]Available[/green]" if info["available"] else "[red]Unavailable[/red]"
        table.add_row(info["name"], info["command"], status)

    console.print(table)


def clear_screen():
    """Clear the terminal screen."""
    console.clear()


def show_document(title: str, content: str):
    """Display a document with markdown rendering."""
    console.print(Panel(
        Markdown(content),
        title=f"[bold cyan]{title}[/bold cyan]",
        border_style="cyan"
    ))


def show_document_list(documents: list):
    """Display a list of documents in the library."""
    if not documents:
        show_info("No documents found in docs/library")
        return

    table = Table(title="Document Library", show_header=True, header_style="bold cyan")
    table.add_column("Name", style="green")
    table.add_column("Title")
    table.add_column("Type", style="dim")

    for doc in documents:
        table.add_row(doc["name"], doc["title"][:50], doc["type"])

    console.print(table)


def show_search_results(results: list, query: str):
    """Display search results."""
    if not results:
        show_info(f"No results found for '{query}'")
        return

    console.print(f"\n[bold]Search results for '[cyan]{query}[/cyan]':[/bold]\n")

    for i, result in enumerate(results, 1):
        console.print(f"[bold green]{i}. {result.name}[/bold green]")
        console.print(f"   [dim]{result.title}[/dim]")
        console.print(f"   {result.snippet}\n")


def show_command_table(tool: str, commands: list):
    """Display CLI commands as a Rich table."""
    if not commands:
        show_info(f"No commands found for {tool}")
        return

    table = Table(
        title=f"{tool.title()} CLI Commands",
        show_header=True,
        header_style="bold cyan"
    )
    table.add_column("Command", style="green", no_wrap=True)
    table.add_column("Description")

    for cmd in commands[:25]:  # Limit to 25 commands
        table.add_row(f"`{cmd.command}`", cmd.description[:80])

    console.print(table)

    if len(commands) > 25:
        console.print(f"[dim]...and {len(commands) - 25} more commands[/dim]")


def show_tools_overview(overviews: list):
    """Display overview of all CLI tools."""
    console.print("\n[bold cyan]CLI Tools Overview[/bold cyan]\n")

    for overview in overviews:
        console.print(f"[bold green]{overview.name}[/bold green] ({overview.tool_id})")
        console.print(f"  {overview.description}")
        console.print(f"  [dim]{len(overview.commands)} commands available[/dim]\n")

    console.print("[dim]Use /ref <tool> for detailed commands[/dim]")


def show_workflow_overview(text: str):
    """Display the workflow overview."""
    console.print(Panel(
        Markdown(text),
        title="[bold cyan]3-Model Workflow[/bold cyan]",
        border_style="cyan"
    ))


def show_workflow_diagram(diagram: str):
    """Display the ASCII workflow diagram."""
    console.print(Panel(
        Text(diagram, style="cyan"),
        title="[bold]Workflow Diagram[/bold]",
        border_style="blue"
    ))


def show_role_info(role):
    """Display detailed role information for a tool."""
    content = f"""## {role.role_title}
**Tool:** {role.name} (`{role.tool_id}`)

**Description:** {role.description}

**Key Strengths:**
"""
    for strength in role.key_strengths:
        content += f"- {strength}\n"

    content += "\n**Typical Tasks:**\n"
    for task in role.typical_tasks:
        content += f"- \"{task}\"\n"

    content += f"\n**Deliverable:** {role.deliverable}"

    if role.usage_note:
        content += f"\n\n**Note:** {role.usage_note}"

    console.print(Panel(
        Markdown(content),
        title=f"[bold cyan]{role.name} Role[/bold cyan]",
        border_style="cyan"
    ))


def show_handoff_advice(advice: str):
    """Display handoff advice between tools."""
    console.print(Panel(
        Markdown(advice),
        title="[bold]Handoff Guide[/bold]",
        border_style="yellow"
    ))
