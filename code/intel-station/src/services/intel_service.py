"""Intel service — loads and caches intel files with YAML frontmatter."""

import logging
from functools import lru_cache

import yaml

from src.config.settings import INTEL_PATH

logger = logging.getLogger(__name__)


@lru_cache(maxsize=128)
def load_intel(relative_path: str) -> dict | None:
    """Load an intel file, parsing YAML frontmatter and markdown body.

    Args:
        relative_path: Path relative to project root, e.g. 'intel/phase1/field_report_001-sandstorm.md'

    Returns:
        Dict with 'frontmatter' (dict) and 'body' (str), or None if file not found.
    """
    # relative_path is like "intel/phase1/file.md" — strip the "intel/" prefix
    # to get the path relative to INTEL_PATH
    if relative_path.startswith("intel/"):
        sub_path = relative_path[len("intel/"):]
    else:
        sub_path = relative_path

    file_path = INTEL_PATH / sub_path

    if not file_path.exists():
        logger.warning("Intel file not found: %s", file_path)
        return None

    try:
        content = file_path.read_text(encoding="utf-8")
    except OSError:
        logger.error("Failed to read intel file: %s", file_path, exc_info=True)
        return None

    frontmatter, body = _parse_frontmatter(content)
    return {"frontmatter": frontmatter, "body": body}


def _parse_frontmatter(content: str) -> tuple[dict, str]:
    """Split YAML frontmatter from markdown body.

    Returns (frontmatter_dict, body_string). If no frontmatter found,
    returns ({}, full_content).
    """
    if not content.startswith("---"):
        return {}, content

    # Find the closing ---
    end_idx = content.find("---", 3)
    if end_idx == -1:
        return {}, content

    yaml_str = content[3:end_idx].strip()
    body = content[end_idx + 3:].lstrip("\n")

    try:
        frontmatter = yaml.safe_load(yaml_str) or {}
    except yaml.YAMLError:
        logger.warning("Failed to parse YAML frontmatter", exc_info=True)
        return {}, content

    return frontmatter, body
