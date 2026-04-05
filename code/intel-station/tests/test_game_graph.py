"""Tests for game_graph structural integrity.

Validates that the graph is well-formed, all references resolve, all intel
files exist on disk, and critical intel is correctly flagged.
"""

from src.config.game_graph import GAME_GRAPH, CRITICAL_INTEL, PHASE_CONCLUSIONS
from src.config.settings import INTEL_PATH


# ── Structural integrity ──────────────────────────────────────────────

class TestGraphStructure:
    def test_start_node_exists(self):
        assert "start" in GAME_GRAPH

    def test_start_has_questions(self):
        assert len(GAME_GRAPH["start"]["questions"]) >= 2

    def test_all_question_references_exist(self):
        """Every node ID referenced in a 'questions' list must exist in the graph."""
        missing = []
        for node_id, node in GAME_GRAPH.items():
            for q in node.get("questions", []):
                if q not in GAME_GRAPH:
                    missing.append((node_id, q))
        assert missing == [], f"Broken question references: {missing}"

    def test_no_self_referencing_questions(self):
        """No node should list itself in its own questions."""
        self_refs = [
            nid for nid, node in GAME_GRAPH.items()
            if nid in node.get("questions", [])
        ]
        assert self_refs == [], f"Self-references found: {self_refs}"

    def test_non_start_nodes_have_required_fields(self):
        """Every non-start node must have label, phase, response, dead_end."""
        required = {"label", "phase", "response", "dead_end"}
        bad = []
        for node_id, node in GAME_GRAPH.items():
            if node_id == "start":
                continue
            missing_fields = required - set(node.keys())
            if missing_fields:
                bad.append((node_id, missing_fields))
        assert bad == [], f"Nodes missing fields: {bad}"

    def test_dead_end_nodes_have_no_outgoing_questions(self):
        for node_id, node in GAME_GRAPH.items():
            if node.get("dead_end"):
                assert node.get("questions", []) == [], (
                    f"Dead-end node {node_id} has outgoing questions"
                )

    def test_dead_end_nodes_have_message(self):
        """Dead-end nodes should have dead_end_message for the UI."""
        for node_id, node in GAME_GRAPH.items():
            if node.get("dead_end"):
                assert node.get("dead_end_message"), (
                    f"Dead-end {node_id} missing dead_end_message"
                )

    def test_all_non_dead_end_non_conclusion_nodes_have_questions(self):
        """Normal nodes (not dead ends, not conclusions) should have follow-ups."""
        for node_id, node in GAME_GRAPH.items():
            if node_id == "start":
                continue
            if node.get("dead_end") or node.get("phase_complete") is not None:
                continue
            # q_decrypt_registry leads to conclusion injected by game_service
            if node_id == "q_decrypt_registry":
                continue
            assert len(node.get("questions", [])) > 0, (
                f"Node {node_id} has no outgoing questions"
            )


# ── Intel file references ─────────────────────────────────────────────

class TestIntelFileReferences:
    def _all_intel_paths(self):
        paths = set()
        for node in GAME_GRAPH.values():
            for p in node.get("intel", []):
                paths.add(p)
        return paths

    def test_all_intel_files_exist_on_disk(self):
        """Every intel path in the graph must point to a real file."""
        missing = []
        for path in self._all_intel_paths():
            sub = path[len("intel/"):] if path.startswith("intel/") else path
            if not (INTEL_PATH / sub).exists():
                missing.append(path)
        assert missing == [], f"Intel files not found: {missing}"

    def test_intel_paths_follow_convention(self):
        """All intel paths should start with 'intel/phase{N}/'."""
        bad = [p for p in self._all_intel_paths() if not p.startswith("intel/phase")]
        assert bad == [], f"Non-standard intel paths: {bad}"

    def test_intel_references_not_empty(self):
        """Graph should reference at least some intel files."""
        assert len(self._all_intel_paths()) > 0


# ── Critical intel ────────────────────────────────────────────────────

class TestCriticalIntel:
    def test_critical_intel_files_exist(self):
        for phase, paths in CRITICAL_INTEL.items():
            for path in paths:
                sub = path[len("intel/"):] if path.startswith("intel/") else path
                assert (INTEL_PATH / sub).exists(), (
                    f"Critical intel missing: phase {phase} -> {path}"
                )

    def test_critical_intel_marked_in_frontmatter(self):
        """Every critical intel file should have critical: true in YAML frontmatter."""
        from src.services.intel_service import load_intel

        for phase, paths in CRITICAL_INTEL.items():
            for path in paths:
                data = load_intel(path)
                assert data is not None, f"Cannot load {path}"
                assert data["frontmatter"].get("critical") is True, (
                    f"{path} not marked critical in frontmatter"
                )

    def test_critical_intel_reachable_from_start(self):
        """All critical intel must be reachable by traversing from start."""
        reachable_intel = set()
        visited = set()
        queue = list(GAME_GRAPH["start"]["questions"])

        while queue:
            nid = queue.pop(0)
            if nid in visited:
                continue
            visited.add(nid)
            node = GAME_GRAPH.get(nid, {})
            for p in node.get("intel", []):
                reachable_intel.add(p)
            for q in node.get("questions", []):
                queue.append(q)

        for phase, paths in CRITICAL_INTEL.items():
            for path in paths:
                assert path in reachable_intel, (
                    f"Critical file {path} not reachable from start"
                )

    def test_phase1_has_critical_intel(self):
        assert len(CRITICAL_INTEL.get(1, [])) > 0


# ── Phase conclusions ─────────────────────────────────────────────────

class TestPhaseConclusions:
    def test_conclusion_nodes_exist(self):
        for phase, node_id in PHASE_CONCLUSIONS.items():
            assert node_id in GAME_GRAPH

    def test_conclusion_nodes_have_phase_complete(self):
        for phase, node_id in PHASE_CONCLUSIONS.items():
            node = GAME_GRAPH[node_id]
            assert node.get("phase_complete") == phase

    def test_conclusion_nodes_are_terminal(self):
        """Conclusion nodes should have the questions field."""
        for phase, node_id in PHASE_CONCLUSIONS.items():
            assert "questions" in GAME_GRAPH[node_id]


# ── Reachability ──────────────────────────────────────────────────────

class TestReachability:
    def test_all_nodes_reachable_from_start(self):
        """Every node should be reachable from start (except phase 2/3 conclusions)."""
        reachable = {"start"}
        queue = list(GAME_GRAPH["start"]["questions"])

        while queue:
            nid = queue.pop(0)
            if nid in reachable:
                continue
            reachable.add(nid)
            node = GAME_GRAPH.get(nid, {})
            for q in node.get("questions", []):
                queue.append(q)

        unreachable = set(GAME_GRAPH.keys()) - reachable
        expected_unreachable = {"q_phase1_conclusion", "q_phase2_conclusion", "q_phase3_conclusion"}
        unexpected = unreachable - expected_unreachable
        assert unexpected == set(), f"Unreachable nodes: {unexpected}"

    def test_all_phase1_intel_files_reachable(self):
        """Every .md file in intel/phase1/ should be referenced by at least one node."""
        phase1_dir = INTEL_PATH / "phase1"
        disk_files = {
            f"intel/phase1/{f.name}"
            for f in phase1_dir.iterdir()
            if f.suffix == ".md"
        }
        graph_files = set()
        for node in GAME_GRAPH.values():
            for p in node.get("intel", []):
                if p.startswith("intel/phase1/"):
                    graph_files.add(p)

        unreferenced = disk_files - graph_files
        assert unreferenced == set(), (
            f"Phase 1 intel on disk but not in graph: {unreferenced}"
        )
