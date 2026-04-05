"""Tests for the intel_service — YAML frontmatter parsing and file loading."""

import pytest

from src.config.settings import INTEL_PATH
from src.services.intel_service import load_intel, _parse_frontmatter


# ── Frontmatter parser ────────────────────────────────────────────────

class TestParseFrontmatter:
    def test_standard_frontmatter(self):
        content = '---\nid: "test"\ntype: "field_report"\n---\n# Title\nBody text'
        fm, body = _parse_frontmatter(content)
        assert fm["id"] == "test"
        assert fm["type"] == "field_report"
        assert body.startswith("# Title")

    def test_no_frontmatter(self):
        content = "# Just a markdown file\nNo frontmatter here."
        fm, body = _parse_frontmatter(content)
        assert fm == {}
        assert body == content

    def test_unclosed_frontmatter(self):
        content = "---\nid: broken\nNo closing delimiter"
        fm, body = _parse_frontmatter(content)
        assert fm == {}
        assert body == content

    def test_empty_frontmatter(self):
        content = "---\n---\n# Body"
        fm, body = _parse_frontmatter(content)
        assert fm == {}
        assert "# Body" in body

    def test_frontmatter_with_metadata(self):
        content = (
            '---\n'
            'id: "fr_001"\n'
            'type: "field_report"\n'
            'critical: true\n'
            'metadata:\n'
            '  filed_by: "Agent FALCON"\n'
            '---\n'
            '# Report\nDetails here.'
        )
        fm, body = _parse_frontmatter(content)
        assert fm["id"] == "fr_001"
        assert fm["critical"] is True
        assert fm["metadata"]["filed_by"] == "Agent FALCON"
        assert body.startswith("# Report")

    def test_invalid_yaml_returns_empty(self):
        content = "---\n: [invalid yaml\n---\nBody"
        fm, body = _parse_frontmatter(content)
        # Should fall back to full content
        assert fm == {}
        assert body == content


# ── File loading ──────────────────────────────────────────────────────

class TestLoadIntel:
    def test_load_existing_phase1_file(self):
        data = load_intel("intel/phase1/field_report_001-sandstorm.md")
        assert data is not None
        assert "frontmatter" in data
        assert "body" in data
        assert data["frontmatter"]["type"] == "field_report"

    def test_load_nonexistent_file(self):
        data = load_intel("intel/phase1/does_not_exist.md")
        assert data is None

    def test_load_phase2_file(self):
        data = load_intel("intel/phase2/corporate_intel_001.md")
        assert data is not None
        assert data["frontmatter"]["phase"] == 2

    def test_load_phase3_file(self):
        data = load_intel("intel/phase3/security_spec_001.md")
        assert data is not None
        assert data["frontmatter"]["phase"] == 3

    def test_frontmatter_has_required_keys(self):
        """Spot-check that loaded files have the expected frontmatter schema."""
        data = load_intel("intel/phase1/intercepted_comm_002.md")
        assert data is not None
        fm = data["frontmatter"]
        for key in ("id", "type", "title", "classification", "reference", "phase", "critical"):
            assert key in fm, f"Missing frontmatter key: {key}"

    def test_body_is_not_empty(self):
        data = load_intel("intel/phase1/field_report_001-sandstorm.md")
        assert data is not None
        assert len(data["body"].strip()) > 0


# ── All intel files loadable ──────────────────────────────────────────

class TestAllIntelFiles:
    @pytest.fixture()
    def all_intel_files(self):
        """Collect all .md files across all phase directories."""
        files = []
        for phase_dir in sorted(INTEL_PATH.iterdir()):
            if phase_dir.is_dir() and phase_dir.name.startswith("phase"):
                for f in sorted(phase_dir.iterdir()):
                    if f.suffix == ".md":
                        rel = f"intel/{phase_dir.name}/{f.name}"
                        files.append(rel)
        return files

    def test_all_files_have_frontmatter(self, all_intel_files):
        """Every intel .md file should parse with non-empty frontmatter."""
        bad = []
        for path in all_intel_files:
            data = load_intel(path)
            if data is None or not data["frontmatter"]:
                bad.append(path)
        assert bad == [], f"Files missing or lacking frontmatter: {bad}"

    def test_all_files_have_id(self, all_intel_files):
        bad = []
        for path in all_intel_files:
            data = load_intel(path)
            if data and not data["frontmatter"].get("id"):
                bad.append(path)
        assert bad == [], f"Files missing 'id' in frontmatter: {bad}"

    def test_all_files_have_type(self, all_intel_files):
        bad = []
        for path in all_intel_files:
            data = load_intel(path)
            if data and not data["frontmatter"].get("type"):
                bad.append(path)
        assert bad == [], f"Files missing 'type' in frontmatter: {bad}"
