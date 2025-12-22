"""Task routing logic for Terminal AI Workflow CLI."""

import re
from dataclasses import dataclass
from typing import List, Tuple, Optional
from .config import get_config
from .errors import NoAvailableToolError, RoutingError


@dataclass
class Route:
    """A single routing result."""
    tool: str
    task: str
    tool_display_name: str
    matched_keyword: Optional[str] = None
    matched_role: Optional[str] = None


def split_sentences(text: str) -> List[str]:
    """Split input text into sentences."""
    # Split by sentence-ending punctuation
    sentences = re.split(r'[.!?]+', text)
    # Clean up and filter empty strings
    return [s.strip() for s in sentences if s.strip()]


def get_first_word(sentence: str) -> str:
    """Extract the first word from a sentence."""
    words = sentence.split()
    return words[0].lower() if words else ""


def find_keyword_match(sentence: str, keywords: List[str]) -> Optional[str]:
    """Find the first matching keyword in a sentence.

    Supports multi-word matching and matches anywhere in the sentence.

    Args:
        sentence: The sentence to search
        keywords: List of keywords to match

    Returns:
        The matched keyword or None
    """
    sentence_lower = sentence.lower()
    words = sentence_lower.split()

    # First, check first word (highest priority)
    if words:
        first_word = words[0]
        for keyword in keywords:
            if first_word == keyword.lower():
                return keyword

    # Then check if any keyword appears anywhere in the sentence
    for keyword in keywords:
        keyword_lower = keyword.lower()
        # Match as a whole word (not as substring of another word)
        pattern = r'\b' + re.escape(keyword_lower) + r'\b'
        if re.search(pattern, sentence_lower):
            return keyword

    return None


def route_sentence(sentence: str, strict: bool = False) -> Route:
    """Route a single sentence to the appropriate tool.

    Uses enhanced keyword matching that:
    1. Prioritizes first-word matches
    2. Falls back to matching anywhere in the sentence
    3. Supports multi-word phrases

    Args:
        sentence: The sentence to route
        strict: If True, raise NoAvailableToolError when no tools available

    Returns:
        Route with tool assignment

    Raises:
        NoAvailableToolError: If strict=True and no tools are available
    """
    config = get_config()

    matched_tool = None
    matched_role = None
    matched_keyword = None

    # Check each role for keyword match
    for role_name, role in config.roles.items():
        match = find_keyword_match(sentence, role.keywords)
        if match:
            # Found a matching role
            matched_role = role_name
            matched_keyword = match
            primary = role.primary
            if config.is_tool_available(primary):
                matched_tool = primary
            else:
                # Try fallbacks
                for fallback in role.fallback:
                    if config.is_tool_available(fallback):
                        matched_tool = fallback
                        break
            break

    # Default fallback chain if no keyword match or matched tool unavailable
    if matched_tool is None:
        default_chain = ["claude", "openai", "gemini"]
        for tool in default_chain:
            if config.is_tool_available(tool):
                matched_tool = tool
                break

    # Handle case where no tools are available
    if matched_tool is None:
        if strict:
            raise NoAvailableToolError()
        # Last resort - use claude even if not authenticated
        matched_tool = "claude"

    # Get display name
    tool_display = config.tools.get(matched_tool)
    display_name = tool_display.name if tool_display else matched_tool.title()

    return Route(
        tool=matched_tool,
        task=sentence,
        tool_display_name=display_name,
        matched_keyword=matched_keyword,
        matched_role=matched_role
    )


def route_input(text: str) -> List[Route]:
    """Route input text to appropriate tools.

    Returns a list of (tool, task) tuples.
    """
    sentences = split_sentences(text)

    if not sentences:
        # If no sentences parsed, treat entire input as one task
        return [route_sentence(text)]

    routes = []
    for sentence in sentences:
        route = route_sentence(sentence)
        routes.append(route)

    return routes


def consolidate_routes(routes: List[Route]) -> List[Route]:
    """Consolidate routes by tool, combining tasks for the same tool."""
    from collections import defaultdict

    tool_tasks = defaultdict(list)
    tool_display = {}

    for route in routes:
        tool_tasks[route.tool].append(route.task)
        tool_display[route.tool] = route.tool_display_name

    consolidated = []
    for tool, tasks in tool_tasks.items():
        combined_task = ". ".join(tasks)
        consolidated.append(Route(
            tool=tool,
            task=combined_task,
            tool_display_name=tool_display[tool]
        ))

    return consolidated
