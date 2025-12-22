"""Knowledge module for Document Library integration.

Provides document indexing, CLI command reference parsing, and workflow strategy access.
"""

from .index import DocumentIndex, search_documents, get_document, refresh_index
from .commands import get_commands, search_commands, get_all_tools_overview
from .workflow import get_role_info, get_workflow_overview, get_handoff_advice, get_all_roles

__all__ = [
    # Document indexing
    "DocumentIndex",
    "search_documents",
    "get_document",
    "refresh_index",
    # CLI commands
    "get_commands",
    "search_commands",
    "get_all_tools_overview",
    # Workflow
    "get_role_info",
    "get_workflow_overview",
    "get_handoff_advice",
    "get_all_roles",
]
