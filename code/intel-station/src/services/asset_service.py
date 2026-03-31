"""Asset service — loads and serves media assets for the Data Viewer."""

from pathlib import Path

from src.config.settings import ASSETS_PATH
from src.config.phases import PHASES, get_all_asset_keys

# Mapping of asset keys to display metadata
ASSET_MANIFEST = {}


def _build_manifest():
    """Build the asset manifest from phase definitions."""
    global ASSET_MANIFEST
    if ASSET_MANIFEST:
        return

    for phase_num, phase_data in PHASES.items():
        for substep_num, substep_data in phase_data["substeps"].items():
            for asset_key in substep_data["assets_to_unlock"]:
                ASSET_MANIFEST[asset_key] = {
                    "phase": phase_num,
                    "substep": substep_num,
                    "path": ASSETS_PATH / asset_key,
                    "type": _detect_type(asset_key),
                    "label": _make_label(asset_key),
                }


def _detect_type(asset_key: str) -> str:
    """Detect asset type from file extension."""
    ext = Path(asset_key).suffix.lower()
    type_map = {
        ".md": "text",
        ".txt": "text",
        ".png": "image",
        ".jpg": "image",
        ".jpeg": "image",
        ".svg": "image",
        ".mp3": "audio",
        ".wav": "audio",
        ".mp4": "video",
        ".webm": "video",
        ".json": "data",
    }
    return type_map.get(ext, "unknown")


def _make_label(asset_key: str) -> str:
    """Generate a human-readable label from an asset key."""
    name = Path(asset_key).stem
    # Replace underscores/hyphens with spaces and title-case
    label = name.replace("_", " ").replace("-", " ").title()
    return label


def get_manifest() -> dict:
    """Get the full asset manifest."""
    _build_manifest()
    return ASSET_MANIFEST


def get_asset_info(asset_key: str) -> dict | None:
    """Get info for a specific asset."""
    _build_manifest()
    return ASSET_MANIFEST.get(asset_key)


def get_asset_path(asset_key: str) -> Path | None:
    """Get the filesystem path for an asset."""
    info = get_asset_info(asset_key)
    if not info:
        return None
    return info["path"]


def read_text_asset(asset_key: str) -> str | None:
    """Read a text/markdown asset and return its content."""
    path = get_asset_path(asset_key)
    if not path or not path.exists():
        return None
    return path.read_text(encoding="utf-8")


def get_assets_for_display(unlocked_keys: list[str]) -> list[dict]:
    """
    Get all assets organized for display, marking locked/unlocked status.

    Returns a list of dicts with asset info + locked status.
    """
    _build_manifest()
    result = []
    all_keys = get_all_asset_keys()

    for key in all_keys:
        info = ASSET_MANIFEST.get(key, {})
        result.append({
            "key": key,
            "label": info.get("label", key),
            "type": info.get("type", "unknown"),
            "phase": info.get("phase", 0),
            "substep": info.get("substep", 0),
            "unlocked": key in unlocked_keys,
            "path": info.get("path"),
        })

    return result
