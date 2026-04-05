"""Deterministic game logic — processes question selections and manages progression."""

import logging
from src.config.game_graph import GAME_GRAPH, CRITICAL_INTEL, PHASE_CONCLUSIONS
from src.services import database_service as db

logger = logging.getLogger(__name__)


def get_node(node_id: str) -> dict | None:
    """Return a graph node by ID, or None if not found."""
    return GAME_GRAPH.get(node_id)


def get_start_questions() -> list[str]:
    """Return the starting question IDs from the root node."""
    return GAME_GRAPH["start"]["questions"]


def process_question(user_id: int, node_id: str, phase: int) -> dict | None:
    """Process a question selection: record intel access and return the node.

    Returns the node dict, or None if the node_id is invalid.
    """
    node = get_node(node_id)
    if node is None:
        logger.warning("Invalid node_id: %s", node_id)
        return None

    for intel_path in node.get("intel", []):
        filename = intel_path.rsplit("/", 1)[-1]
        category = _category_from_path(intel_path)
        db.record_document_access(user_id, filename, category, phase)

    return node


def get_available_questions(node_id: str, visited_nodes: set[str]) -> list[str]:
    """Return the question IDs available from a node, filtering already-visited ones.

    For dead-end nodes (no outgoing questions), returns nothing — the UI
    handles showing the parent's remaining unvisited questions.
    """
    node = get_node(node_id)
    if node is None:
        return []
    return [q for q in node.get("questions", []) if q not in visited_nodes]


def get_parent_unvisited_questions(node_id: str, visited_nodes: set[str]) -> list[str]:
    """For dead-end nodes, find the parent and return its unvisited questions."""
    for parent_id, parent in GAME_GRAPH.items():
        if parent_id == "start":
            continue
        if node_id in parent.get("questions", []):
            return [q for q in parent["questions"] if q not in visited_nodes and q != node_id]
    return []


def check_phase_completion_available(user_id: int, phase: int) -> str | None:
    """If all critical intel for the phase has been accessed, return the conclusion node ID."""
    critical = CRITICAL_INTEL.get(phase, [])
    if not critical:
        return None

    accessed = set(db.get_accessed_doc_filenames(user_id))
    critical_filenames = {path.rsplit("/", 1)[-1] for path in critical}

    if critical_filenames.issubset(accessed):
        return PHASE_CONCLUSIONS.get(phase)
    return None


def get_missing_critical_intel(user_id: int, phase: int) -> list[str]:
    """Return the critical intel file paths not yet accessed for a phase."""
    critical = CRITICAL_INTEL.get(phase, [])
    if not critical:
        return []

    accessed = set(db.get_accessed_doc_filenames(user_id))
    return [
        path for path in critical
        if path.rsplit("/", 1)[-1] not in accessed
    ]


def reconstruct_visited_nodes(user_id: int) -> set[str]:
    """Rebuild the set of visited node IDs from accessed_documents.

    For each graph node, if ALL of its intel files have been accessed,
    that node is considered visited.
    """
    accessed = set(db.get_accessed_doc_filenames(user_id))
    visited = set()

    for node_id, node in GAME_GRAPH.items():
        if node_id == "start":
            continue
        intel_files = node.get("intel", [])
        if not intel_files:
            # Nodes with no intel (dead ends with no files, conclusions)
            # are tracked purely through session state
            continue
        filenames = {path.rsplit("/", 1)[-1] for path in intel_files}
        if filenames.issubset(accessed):
            visited.add(node_id)

    return visited


def reconstruct_current_node(visited_nodes: set[str]) -> str | None:
    """Determine the last meaningful node the user was at.

    Walks the graph from start, following visited paths, and returns
    the deepest visited node.
    """
    if not visited_nodes:
        return None

    # BFS from start, track the deepest visited node
    current = "start"
    best = None
    queue = list(GAME_GRAPH["start"]["questions"])

    while queue:
        node_id = queue.pop(0)
        if node_id in visited_nodes:
            best = node_id
            node = GAME_GRAPH.get(node_id, {})
            for q in node.get("questions", []):
                if q not in visited_nodes:
                    continue
                queue.append(q)

    return best


def _category_from_path(intel_path: str) -> str:
    """Extract the intel category from a file path like 'intel/phase1/field_report_001-sandstorm.md'."""
    filename = intel_path.rsplit("/", 1)[-1]
    # Strip the numeric suffix and extension: field_report_001-sandstorm.md -> field_report
    parts = filename.split("_")
    # Most types are two words: field_report, intercepted_comm, etc.
    # codename_registry is also two words
    if len(parts) >= 2:
        # Check if the second part starts with a digit → single-word type (shouldn't happen)
        # Otherwise join first two parts
        if parts[1][0].isdigit():
            return parts[0]
        return f"{parts[0]}_{parts[1]}"
    return parts[0]
