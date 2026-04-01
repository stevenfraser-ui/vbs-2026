"""Custom Strands tool for querying the intelligence knowledge base."""

import logging
from pathlib import Path

from strands import tool

from src.config.settings import KB_PATH

logger = logging.getLogger(__name__)

# Category display names
CATEGORY_LABELS = {
    "field_reports": "Field Reports",
    "intercepted_comms": "Intercepted Communications",
    "informant_tips": "Informant Tips",
    "surveillance": "Surveillance & Imagery",
    "hostile_orgs": "Hostile Organization Profiles",
    "tech_analysis": "Technical Analysis",
    "codenames": "Code-Name Registry",
    "transfer_logs": "Transfer Logs",
    "facility_reports": "Facility Reports",
    "corporate_intel": "Corporate Intelligence",
    "energy_analysis": "Energy Analysis",
    "procurement_records": "Procurement Records",
    "shell_companies": "Shell Company Registry",
    "security_specs": "Security Specifications",
    "insider_reports": "Insider Reports",
}

# Documents that require prerequisites before they can be accessed.
# Key: document filename, Value: list of prerequisite document filenames.
ACCESS_GATES = {
    # The decrypted LOGOS registry entry requires that the cross-reference
    # report (tech_analysis_003) has been accessed — proving the agent has
    # the evidence to decrypt it.
    "codename_registry_decrypted.md": ["tech_analysis_003.md"],
    # LOGOS intercepts (comm 002, 004, 005) are findable from the start but
    # sender shows as UNKNOWN-7 until the code name is discovered.
    # No hard gate — the narrative handles this via the UNKNOWN-7 label.
    # Phase 2 gates — breadcrumb trail for location discovery
    "transfer_log_003.md": ["transfer_log_002.md"],
    "energy_analysis_002.md": ["energy_analysis_001.md"],
    "facility_report_004.md": ["energy_analysis_002.md"],
    # Phase 3 gates — shell company → security spec chain
    "shell_company_004.md": ["procurement_record_001.md"],
    "security_spec_001.md": ["shell_company_001.md"],
    "security_spec_002.md": ["shell_company_003.md"],
    "security_spec_003.md": ["shell_company_002.md"],
}


def _load_kb_index() -> dict[str, dict]:
    """Load and index all knowledge base documents.

    Returns a dict keyed by filename with metadata and content.
    """
    index = {}
    if not KB_PATH.exists():
        logger.warning("Knowledge base path does not exist: %s", KB_PATH)
        return index

    for category_dir in sorted(KB_PATH.iterdir()):
        if not category_dir.is_dir():
            continue
        category = category_dir.name
        for doc_path in sorted(category_dir.iterdir()):
            if doc_path.suffix.lower() != ".md":
                continue
            content = doc_path.read_text(encoding="utf-8")
            index[doc_path.name] = {
                "filename": doc_path.name,
                "category": category,
                "category_label": CATEGORY_LABELS.get(category, category),
                "path": str(doc_path),
                "content": content,
            }
    return index


# Module-level cache
_KB_INDEX: dict[str, dict] | None = None

# User context for access gate enforcement — set before each agent call
_current_user_accessed_docs: list[str] = []


def set_user_context(accessed_docs: list[str]) -> None:
    """Set the current user's accessed documents for access gate checks."""
    global _current_user_accessed_docs
    _current_user_accessed_docs = list(accessed_docs)


def clear_user_context() -> None:
    """Clear the user context after the agent call completes."""
    global _current_user_accessed_docs
    _current_user_accessed_docs = []


def _get_index() -> dict[str, dict]:
    global _KB_INDEX
    if _KB_INDEX is None:
        _KB_INDEX = _load_kb_index()
    return _KB_INDEX


def reload_index():
    """Force reload the KB index (useful after changes)."""
    global _KB_INDEX
    _KB_INDEX = None


def get_document(filename: str) -> dict | None:
    """Get a single document by filename."""
    return _get_index().get(filename)


def get_all_categories() -> list[str]:
    """Get all category directory names."""
    return list(CATEGORY_LABELS.keys())


def check_prerequisites(filename: str, accessed_docs: list[str]) -> tuple[bool, list[str]]:
    """Check if prerequisites are met for a gated document.

    Returns (can_access, missing_prereqs).
    """
    prereqs = ACCESS_GATES.get(filename, [])
    if not prereqs:
        return True, []
    missing = [p for p in prereqs if p not in accessed_docs]
    return len(missing) == 0, missing


@tool
def query_intel(query: str, category: str = "") -> str:
    """Search the IMF intelligence knowledge base for documents matching a query.

    Use this tool when an agent asks about The Light, the Architect, LOGOS,
    hostile organizations, field reports, intercepted messages, informant tips,
    facility locations, transfers, energy signatures, corporate intel,
    security systems, floor grid, pressure sensors, shell companies,
    contractors, alarms, or any other mission-related intelligence.

    Args:
        query: Search terms to look for in intelligence documents. Use keywords
               like "the light", "weapon", "designer", "LOGOS", "UNKNOWN-7",
               "server", "software", "code name", "location", "moved",
               "transfer", "facility", "power", "energy", "TITAN",
               "vault", "corporation", "security", "floor", "pressure",
               "grid", "shell company", "contractor", "AEGIS", "alarm",
               "relocation", "pathway", "Frost Veil", "Midnight Sun",
               "Boreal", etc.
        category: Optional. Filter by category: field_reports, intercepted_comms,
                  informant_tips, surveillance, hostile_orgs, tech_analysis, codenames,
                  transfer_logs, facility_reports, corporate_intel, energy_analysis,
                  procurement_records, shell_companies, security_specs, insider_reports.
                  Leave empty to search all categories.
    """
    index = _get_index()
    if not index:
        logger.warning("query_intel called but KB index is empty")
        return "ERROR: Intelligence database is offline. No documents available."

    logger.info(
        "KB query: query=%r category=%r docs_in_index=%d",
        query, category or "all", len(index),
    )

    query_lower = query.lower()
    query_terms = query_lower.split()

    results = []
    for filename, doc in index.items():
        # Category filter
        if category and doc["category"] != category:
            continue

        # Search content and filename for query terms
        content_lower = doc["content"].lower()
        filename_lower = filename.lower()
        searchable = content_lower + " " + filename_lower

        # Score by number of matching terms
        score = sum(1 for term in query_terms if term in searchable)

        if score > 0:
            results.append((score, filename, doc))

    if not results:
        return (
            f"No intelligence documents found matching '{query}'"
            + (f" in category '{category}'" if category else "")
            + ". Try different search terms or broaden your query."
        )

    # Sort by relevance score descending
    results.sort(key=lambda x: x[0], reverse=True)

    # Enforce access gates — filter out gated documents whose prereqs aren't met
    accessible = []
    gated = []
    for score, filename, doc in results:
        can_access, missing = check_prerequisites(filename, _current_user_accessed_docs)
        if can_access:
            accessible.append((score, filename, doc))
        else:
            gated.append((filename, doc, missing))
            logger.info(
                "Access gate denied: doc=%r missing_prereqs=%s",
                filename, missing,
            )

    logger.debug(
        "KB query results: query=%r matched=%d accessible=%d gated=%d",
        query, len(results), len(accessible), len(gated),
    )

    # Return top results (limit to 5 to avoid overwhelming the LLM)
    output_parts = [f"INTEL SEARCH RESULTS for '{query}':"]
    output_parts.append(f"Found {len(accessible)} matching document(s).\n")

    for score, filename, doc in accessible[:5]:
        output_parts.append(f"--- {doc['category_label']} ---")
        output_parts.append(f"Document: {filename}")
        # Include full content so the AI can discuss it
        output_parts.append(doc["content"])
        output_parts.append("")

    if len(accessible) > 5:
        output_parts.append(
            f"({len(accessible) - 5} additional document(s) available. "
            "Narrow your search or specify a category for more targeted results.)"
        )

    # Notify about gated documents so the AI can guide the agent
    if gated:
        output_parts.append("")
        for filename, doc, missing in gated:
            output_parts.append(
                f"[CLASSIFIED] {filename} — prerequisite intelligence not yet "
                f"gathered. Required first: {', '.join(missing)}"
            )

    return "\n".join(output_parts)
