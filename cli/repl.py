"""REPL loop for Terminal AI Workflow CLI."""

import threading
from pathlib import Path
from typing import Optional
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.styles import Style
from prompt_toolkit.completion import WordCompleter
from rich.live import Live
from rich.markdown import Markdown

from . import display
from .router import route_input, consolidate_routes
from .executor import create_workspace, execute_tool_streaming, get_tools_status
from .config import get_config
from .knowledge import (
    search_documents, get_document, refresh_index,
    get_commands, search_commands, get_all_tools_overview,
    get_role_info, get_workflow_overview, get_handoff_advice, get_all_roles
)
from .knowledge.index import list_documents
from .knowledge.workflow import get_workflow_diagram

# Custom prompt style
PROMPT_STYLE = Style.from_dict({
    'prompt': 'bold cyan',
})

# Command completer - now includes documentation commands
COMMANDS = [
    '/help', '/status', '/tasks', '/log', '/clear', '/exit', '/quit',
    '/docs', '/ref', '/workflow'
]
command_completer = WordCompleter(COMMANDS, ignore_case=True)


class REPL:
    """Interactive REPL for Terminal AI Workflow."""

    def __init__(self, history_file: str = ".cli_history", verbose: bool = False):
        self.history_file = Path(history_file)
        self.verbose = verbose
        self.session: Optional[PromptSession] = None
        self.running = False

    def setup(self):
        """Set up the prompt session."""
        self.session = PromptSession(
            history=FileHistory(str(self.history_file)),
            auto_suggest=AutoSuggestFromHistory(),
            completer=command_completer,
            style=PROMPT_STYLE,
            complete_while_typing=False,
        )

    def handle_command(self, command: str) -> bool:
        """Handle a built-in command.

        Returns True if REPL should continue, False to exit.
        """
        cmd = command.strip()
        cmd_lower = cmd.lower()

        if cmd_lower in ('/exit', '/quit'):
            display.console.print("\n[dim]Goodbye![/dim]")
            return False

        elif cmd_lower == '/help':
            display.show_help()

        elif cmd_lower == '/status':
            status = get_tools_status()
            display.show_status(status)

        elif cmd_lower == '/clear':
            display.clear_screen()

        elif cmd_lower == '/tasks':
            self._show_tasks()

        elif cmd_lower == '/log':
            self._show_log()

        elif cmd_lower.startswith('/docs'):
            self._handle_docs(cmd[5:].strip())

        elif cmd_lower.startswith('/ref'):
            self._handle_ref(cmd[4:].strip())

        elif cmd_lower.startswith('/workflow'):
            self._handle_workflow(cmd[9:].strip())

        else:
            display.show_error(f"Unknown command: {command}")

        return True

    def _show_tasks(self):
        """Show current task files."""
        tasks_dir = Path("config/tasks")
        if not tasks_dir.exists():
            display.show_info("No tasks directory found")
            return

        found = False
        for task_file in tasks_dir.glob("*.txt"):
            if task_file.name.startswith("_"):
                continue
            try:
                content = task_file.read_text().strip()
                tool = task_file.stem
                display.console.print(f"[bold cyan]{tool}:[/bold cyan] {content[:100]}")
                found = True
            except Exception:
                pass

        if not found:
            display.show_info("No active tasks")

    def _show_log(self):
        """Show recent log entries."""
        log_file = Path("logs/run.log")
        if not log_file.exists():
            display.show_info("No log file found")
            return

        try:
            lines = log_file.read_text().splitlines()
            recent = lines[-20:] if len(lines) > 20 else lines
            display.console.print("[bold]Recent log entries:[/bold]")
            for line in recent:
                display.console.print(f"[dim]{line}[/dim]")
        except Exception as e:
            display.show_error(f"Could not read log: {e}")

    def _handle_docs(self, args: str):
        """Handle /docs command.

        Usage:
            /docs              - List all documents
            /docs <name>       - Display document content
            /docs search <q>   - Search across documents
            /docs refresh      - Rebuild document index
        """
        if not args:
            # List all documents
            docs = list_documents()
            display.show_document_list(docs)

        elif args.lower() == "refresh":
            # Rebuild index
            display.show_info("Rebuilding document index...")
            count = refresh_index()
            display.show_success(f"Indexed {count} documents")

        elif args.lower().startswith("search "):
            # Search documents
            query = args[7:].strip()
            if query:
                results = search_documents(query)
                display.show_search_results(results, query)
            else:
                display.show_error("Usage: /docs search <query>")

        else:
            # Get specific document
            content = get_document(args)
            if content:
                display.show_document(args, content)
            else:
                display.show_error(f"Document not found: {args}")
                display.show_info("Use /docs to list available documents")

    def _handle_ref(self, args: str):
        """Handle /ref command.

        Usage:
            /ref               - Overview of all CLIs
            /ref claude        - Claude Code commands
            /ref gemini        - Gemini CLI commands
            /ref openai        - OpenAI Codex commands
            /ref <command>     - Search for a command
        """
        if not args:
            # Show overview of all tools
            overviews = get_all_tools_overview()
            display.show_tools_overview(overviews)

        elif args.lower() in ("claude", "gemini", "openai", "codex"):
            # Show commands for specific tool
            tool = "openai" if args.lower() == "codex" else args.lower()
            commands = get_commands(tool)
            display.show_command_table(tool, commands)

        else:
            # Search for a command
            results = search_commands(args)
            if results:
                display.console.print(f"\n[bold]Commands matching '[cyan]{args}[/cyan]':[/bold]\n")
                for cmd in results[:15]:
                    display.console.print(
                        f"  [green]{cmd.tool}[/green]: `{cmd.command}` - {cmd.description[:60]}"
                    )
            else:
                display.show_info(f"No commands found matching '{args}'")

    def _handle_workflow(self, args: str):
        """Handle /workflow command.

        Usage:
            /workflow          - Show workflow overview
            /workflow roles    - Detailed role descriptions
            /workflow <tool>   - Specific tool's role
            /workflow diagram  - ASCII workflow diagram
            /workflow handoff <from> <to> - Handoff advice
        """
        if not args:
            # Show workflow overview
            overview = get_workflow_overview()
            display.show_workflow_overview(overview)

        elif args.lower() == "roles":
            # Show all roles
            for role in get_all_roles():
                display.show_role_info(role)
                display.console.print()

        elif args.lower() == "diagram":
            # Show ASCII diagram
            diagram = get_workflow_diagram()
            display.show_workflow_diagram(diagram)

        elif args.lower().startswith("handoff "):
            # Handoff advice
            parts = args[8:].strip().split()
            if len(parts) >= 2:
                advice = get_handoff_advice(parts[0], parts[1])
                display.show_handoff_advice(advice)
            else:
                display.show_error("Usage: /workflow handoff <from> <to>")
                display.show_info("Example: /workflow handoff gemini claude")

        elif args.lower() in ("claude", "gemini", "openai", "codex"):
            # Show specific tool's role
            tool = "openai" if args.lower() == "codex" else args.lower()
            role = get_role_info(tool)
            if role:
                display.show_role_info(role)
            else:
                display.show_error(f"No role info for {tool}")

    def process_input(self, text: str):
        """Process user input - route and execute."""
        # Route the input
        routes = route_input(text)

        if self.verbose:
            display.show_routing(routes, verbose=True)

        # Consolidate routes by tool
        consolidated = consolidate_routes(routes)

        # Create workspace
        workspace = create_workspace()

        # Execute each tool
        for route in consolidated:
            self._execute_with_live_output(route, workspace)

    def _execute_with_live_output(self, route, workspace):
        """Execute a tool and display output with live markdown rendering."""
        display.show_tool_header(route.tool_display_name)

        # Buffer for accumulating output
        buffer = []
        lock = threading.Lock()

        def on_output(chunk: str):
            """Callback for each output chunk."""
            with lock:
                buffer.append(chunk)

        # We'll use a simpler approach - collect output then display
        # For true streaming, we'd need async, but this works for now
        result = execute_tool_streaming(route, workspace, on_output)

        # Display the final output with markdown rendering
        if result.output.strip():
            display.console.print(Markdown(result.output))

        display.show_tool_footer()

        if self.verbose:
            display.console.print(
                f"[dim]Completed in {result.duration:.1f}s, "
                f"exit code: {result.exit_code}[/dim]"
            )

    def run(self):
        """Run the REPL loop."""
        self.setup()
        self.running = True

        display.show_header()

        while self.running:
            try:
                text = self.session.prompt("> ")

                if not text.strip():
                    continue

                # Check for commands
                if text.strip().startswith('/'):
                    self.running = self.handle_command(text.strip())
                    continue

                # Process as task
                self.process_input(text.strip())

            except KeyboardInterrupt:
                display.console.print("\n[dim]Use /exit to quit[/dim]")
                continue

            except EOFError:
                display.console.print("\n[dim]Goodbye![/dim]")
                break

            except Exception as e:
                display.show_error(str(e))


def run_repl(verbose: bool = False):
    """Create and run a REPL instance."""
    repl = REPL(verbose=verbose)
    repl.run()
