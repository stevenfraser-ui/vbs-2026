"""Tests for the game_service — deterministic game logic."""

import pytest

from src.config.game_graph import GAME_GRAPH, CRITICAL_INTEL
from src.services import game_service


# ── Pure functions (no DB needed) ─────────────────────────────────────

class TestGetNode:
    def test_existing_node(self):
        node = game_service.get_node("q_what_is_light")
        assert node is not None
        assert node["label"] == "What is the Light?"

    def test_start_node(self):
        node = game_service.get_node("start")
        assert node is not None
        assert "questions" in node

    def test_nonexistent_node(self):
        assert game_service.get_node("q_does_not_exist") is None


class TestGetStartQuestions:
    def test_returns_list(self):
        qs = game_service.get_start_questions()
        assert isinstance(qs, list)
        assert len(qs) >= 2

    def test_all_start_questions_exist_in_graph(self):
        for q in game_service.get_start_questions():
            assert q in GAME_GRAPH


class TestGetAvailableQuestions:
    def test_unvisited(self):
        qs = game_service.get_available_questions("q_what_is_light", set())
        assert "q_is_it_weapon" in qs
        assert "q_convoy_contents" in qs
        assert "q_who_wants_it" in qs

    def test_filters_visited(self):
        visited = {"q_is_it_weapon", "q_convoy_contents"}
        qs = game_service.get_available_questions("q_what_is_light", visited)
        assert "q_is_it_weapon" not in qs
        assert "q_convoy_contents" not in qs
        assert "q_who_wants_it" in qs

    def test_all_visited(self):
        node = GAME_GRAPH["q_what_is_light"]
        visited = set(node["questions"])
        qs = game_service.get_available_questions("q_what_is_light", visited)
        assert qs == []

    def test_invalid_node(self):
        assert game_service.get_available_questions("nonexistent", set()) == []

    def test_dead_end_has_no_questions(self):
        qs = game_service.get_available_questions("q_sparrow_lead", set())
        assert qs == []


class TestGetParentUnvisitedQuestions:
    def test_dead_end_returns_sibling_questions(self):
        # q_sparrow_lead is a dead end child of q_is_it_weapon
        visited = {"q_sparrow_lead"}
        qs = game_service.get_parent_unvisited_questions("q_sparrow_lead", visited)
        # Should return the other children of q_is_it_weapon, minus q_sparrow_lead
        parent_node = GAME_GRAPH["q_is_it_weapon"]
        expected = [q for q in parent_node["questions"] if q != "q_sparrow_lead"]
        assert set(qs) == set(expected)

    def test_dead_end_filters_visited_siblings(self):
        visited = {"q_sparrow_lead", "q_meridian_plans"}
        qs = game_service.get_parent_unvisited_questions("q_sparrow_lead", visited)
        assert "q_meridian_plans" not in qs

    def test_node_not_in_any_parent(self):
        # start's children have start as parent, but start is skipped
        qs = game_service.get_parent_unvisited_questions("q_what_is_light", set())
        # start is skipped in the search, so this returns []
        assert qs == []


class TestCategoryFromPath:
    def test_field_report(self):
        assert game_service._category_from_path("intel/phase1/field_report_001-sandstorm.md") == "field_report"

    def test_intercepted_comm(self):
        assert game_service._category_from_path("intel/phase1/intercepted_comm_002.md") == "intercepted_comm"

    def test_codename_registry(self):
        assert game_service._category_from_path("intel/phase1/codename_registry_decrypted.md") == "codename_registry"

    def test_informant_tip(self):
        assert game_service._category_from_path("intel/phase1/informant_tip_001-cobalt.md") == "informant_tip"

    def test_tech_analysis(self):
        assert game_service._category_from_path("intel/phase1/tech_analysis_003.md") == "tech_analysis"

    def test_hostile_org(self):
        assert game_service._category_from_path("intel/phase1/hostile_org_001-meridian.md") == "hostile_org"

    def test_corporate_intel(self):
        assert game_service._category_from_path("intel/phase2/corporate_intel_001.md") == "corporate_intel"

    def test_security_spec(self):
        assert game_service._category_from_path("intel/phase3/security_spec_001.md") == "security_spec"

    def test_shell_company(self):
        assert game_service._category_from_path("intel/phase3/shell_company_004.md") == "shell_company"


class TestReconstructCurrentNode:
    def test_empty_visited(self):
        assert game_service.reconstruct_current_node(set()) is None

    def test_single_visited(self):
        result = game_service.reconstruct_current_node({"q_what_is_light"})
        assert result == "q_what_is_light"

    def test_deep_path(self):
        visited = {"q_what_is_light", "q_is_it_weapon", "q_meridian_plans"}
        result = game_service.reconstruct_current_node(visited)
        # Should return the deepest node
        assert result == "q_meridian_plans"


# ── DB-dependent functions ────────────────────────────────────────────

class TestProcessQuestion:
    def test_process_valid_question(self, tmp_db):
        user = tmp_db.create_user("Test", "1234", 10)
        node = game_service.process_question(user.id, "q_what_is_light", 1)
        assert node is not None
        assert node["label"] == "What is the Light?"

        # Check intel was recorded
        docs = tmp_db.get_accessed_doc_filenames(user.id)
        assert "field_report_001-sandstorm.md" in docs
        assert "informant_tip_001-cobalt.md" in docs

    def test_process_invalid_question(self, tmp_db):
        user = tmp_db.create_user("Test", "1234", 10)
        node = game_service.process_question(user.id, "nonexistent", 1)
        assert node is None

    def test_process_dead_end_with_intel(self, tmp_db):
        user = tmp_db.create_user("Test", "1234", 10)
        node = game_service.process_question(user.id, "q_sparrow_lead", 1)
        assert node is not None
        assert node["dead_end"] is True
        docs = tmp_db.get_accessed_doc_filenames(user.id)
        assert "informant_tip_002-sparrow.md" in docs

    def test_process_dead_end_without_intel(self, tmp_db):
        user = tmp_db.create_user("Test", "1234", 10)
        node = game_service.process_question(user.id, "q_arms_network", 1)
        assert node is not None
        assert node["dead_end"] is True
        docs = tmp_db.get_accessed_doc_filenames(user.id)
        assert len(docs) == 0

    def test_duplicate_processing_idempotent(self, tmp_db):
        user = tmp_db.create_user("Test", "1234", 10)
        game_service.process_question(user.id, "q_what_is_light", 1)
        game_service.process_question(user.id, "q_what_is_light", 1)
        docs = tmp_db.get_accessed_doc_filenames(user.id)
        # Should still just have 2 unique docs, not 4
        assert len(docs) == 2


class TestCheckPhaseCompletion:
    def test_incomplete_phase(self, tmp_db):
        user = tmp_db.create_user("Test", "1234", 10)
        result = game_service.check_phase_completion_available(user.id, 1)
        assert result is None

    def test_complete_phase1(self, tmp_db):
        user = tmp_db.create_user("Test", "1234", 10)
        # Record all critical intel
        for path in CRITICAL_INTEL[1]:
            filename = path.rsplit("/", 1)[-1]
            tmp_db.record_document_access(user.id, filename, "test", 1)

        result = game_service.check_phase_completion_available(user.id, 1)
        assert result == "q_phase1_conclusion"

    def test_partial_critical_intel(self, tmp_db):
        user = tmp_db.create_user("Test", "1234", 10)
        # Record only some critical intel
        path = CRITICAL_INTEL[1][0]
        filename = path.rsplit("/", 1)[-1]
        tmp_db.record_document_access(user.id, filename, "test", 1)

        result = game_service.check_phase_completion_available(user.id, 1)
        assert result is None

    def test_empty_critical_intel_phase(self, tmp_db):
        user = tmp_db.create_user("Test", "1234", 10)
        # Phase 2 has no critical intel yet
        result = game_service.check_phase_completion_available(user.id, 2)
        assert result is None


class TestGetMissingCriticalIntel:
    def test_none_collected(self, tmp_db):
        user = tmp_db.create_user("Test", "1234", 10)
        missing = game_service.get_missing_critical_intel(user.id, 1)
        assert len(missing) == len(CRITICAL_INTEL[1])

    def test_all_collected(self, tmp_db):
        user = tmp_db.create_user("Test", "1234", 10)
        for path in CRITICAL_INTEL[1]:
            filename = path.rsplit("/", 1)[-1]
            tmp_db.record_document_access(user.id, filename, "test", 1)
        missing = game_service.get_missing_critical_intel(user.id, 1)
        assert missing == []


class TestReconstructVisitedNodes:
    def test_empty_user(self, tmp_db):
        user = tmp_db.create_user("Test", "1234", 10)
        visited = game_service.reconstruct_visited_nodes(user.id)
        assert visited == set()

    def test_after_processing_questions(self, tmp_db):
        user = tmp_db.create_user("Test", "1234", 10)
        game_service.process_question(user.id, "q_what_is_light", 1)
        visited = game_service.reconstruct_visited_nodes(user.id)
        assert "q_what_is_light" in visited

    def test_node_with_shared_intel(self, tmp_db):
        """Nodes sharing intel files: both marked visited when all files accessed."""
        user = tmp_db.create_user("Test", "1234", 10)
        # q_intercepted_transmissions and q_source_code both reference intercepted_comm_005
        game_service.process_question(user.id, "q_intercepted_transmissions", 1)
        game_service.process_question(user.id, "q_source_code", 1)
        visited = game_service.reconstruct_visited_nodes(user.id)
        assert "q_intercepted_transmissions" in visited
        assert "q_source_code" in visited
