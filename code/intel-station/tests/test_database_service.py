"""Tests for database_service — CRUD ops, document access, progress reset."""

import pytest


class TestUserCRUD:
    def test_create_user(self, tmp_db):
        user = tmp_db.create_user("Alice", "1111", 8)
        assert user.id is not None
        assert user.name == "Alice"
        assert user.code == "1111"
        assert user.age == 8
        assert user.current_phase == 1
        assert user.completed is False

    def test_get_user_by_code(self, tmp_db):
        tmp_db.create_user("Bob", "2222", 10)
        user = tmp_db.get_user_by_code("2222")
        assert user is not None
        assert user.name == "Bob"

    def test_get_user_by_code_not_found(self, tmp_db):
        assert tmp_db.get_user_by_code("9999") is None

    def test_get_user_by_id(self, tmp_db):
        created = tmp_db.create_user("Carol", "3333", 6)
        user = tmp_db.get_user_by_id(created.id)
        assert user is not None
        assert user.name == "Carol"

    def test_get_all_users(self, tmp_db):
        tmp_db.create_user("Alice", "1111", 8)
        tmp_db.create_user("Bob", "2222", 10)
        users = tmp_db.get_all_users()
        assert len(users) == 2
        names = [u.name for u in users]
        assert "Alice" in names
        assert "Bob" in names

    def test_update_user_phase(self, tmp_db):
        user = tmp_db.create_user("Test", "1234", 10)
        updated = tmp_db.update_user(user.id, current_phase=2)
        assert updated.current_phase == 2

    def test_update_user_completed(self, tmp_db):
        user = tmp_db.create_user("Test", "1234", 10)
        updated = tmp_db.update_user(user.id, completed=True)
        assert updated.completed is True

    def test_update_user_disallowed_field(self, tmp_db):
        user = tmp_db.create_user("Test", "1234", 10)
        # 'id' is not in the allowed set
        updated = tmp_db.update_user(user.id, id=999)
        assert updated.id == user.id  # unchanged

    def test_delete_user(self, tmp_db):
        user = tmp_db.create_user("Test", "1234", 10)
        assert tmp_db.delete_user(user.id) is True
        assert tmp_db.get_user_by_id(user.id) is None

    def test_delete_nonexistent_user(self, tmp_db):
        assert tmp_db.delete_user(99999) is False

    def test_unique_code_constraint(self, tmp_db):
        tmp_db.create_user("Alice", "1111", 8)
        with pytest.raises(Exception):
            tmp_db.create_user("Bob", "1111", 10)


class TestDocumentAccess:
    def test_record_and_get(self, tmp_db):
        user = tmp_db.create_user("Test", "1234", 10)
        tmp_db.record_document_access(user.id, "field_report_001.md", "field_report", 1)
        docs = tmp_db.get_accessed_documents(user.id)
        assert len(docs) == 1
        assert docs[0]["doc_filename"] == "field_report_001.md"
        assert docs[0]["category"] == "field_report"
        assert docs[0]["phase"] == 1

    def test_duplicate_access_ignored(self, tmp_db):
        user = tmp_db.create_user("Test", "1234", 10)
        tmp_db.record_document_access(user.id, "file.md", "test", 1)
        tmp_db.record_document_access(user.id, "file.md", "test", 1)
        docs = tmp_db.get_accessed_documents(user.id)
        assert len(docs) == 1

    def test_get_accessed_doc_filenames(self, tmp_db):
        user = tmp_db.create_user("Test", "1234", 10)
        tmp_db.record_document_access(user.id, "a.md", "cat", 1)
        tmp_db.record_document_access(user.id, "b.md", "cat", 1)
        filenames = tmp_db.get_accessed_doc_filenames(user.id)
        assert set(filenames) == {"a.md", "b.md"}

    def test_get_accessed_documents_for_phase(self, tmp_db):
        user = tmp_db.create_user("Test", "1234", 10)
        tmp_db.record_document_access(user.id, "p1.md", "cat", 1)
        tmp_db.record_document_access(user.id, "p2.md", "cat", 2)
        phase1 = tmp_db.get_accessed_documents_for_phase(user.id, 1)
        assert len(phase1) == 1
        assert phase1[0]["doc_filename"] == "p1.md"

    def test_cascade_delete(self, tmp_db):
        user = tmp_db.create_user("Test", "1234", 10)
        tmp_db.record_document_access(user.id, "file.md", "cat", 1)
        tmp_db.delete_user(user.id)
        # Foreign key cascade should remove documents too
        docs = tmp_db.get_accessed_documents(user.id)
        assert len(docs) == 0


class TestProgressReset:
    def test_reset_user_progress(self, tmp_db):
        user = tmp_db.create_user("Test", "1234", 10)
        tmp_db.update_user(user.id, current_phase=3, completed=True)
        tmp_db.record_document_access(user.id, "file.md", "cat", 1)

        reset = tmp_db.reset_user_progress(user.id)
        assert reset.current_phase == 1
        assert reset.completed is False
        assert tmp_db.get_accessed_documents(user.id) == []

    def test_reset_all_progress(self, tmp_db):
        u1 = tmp_db.create_user("A", "1111", 8)
        u2 = tmp_db.create_user("B", "2222", 10)
        tmp_db.update_user(u1.id, current_phase=2)
        tmp_db.update_user(u2.id, current_phase=3)
        tmp_db.record_document_access(u1.id, "file.md", "cat", 1)

        tmp_db.reset_all_progress()

        for uid in [u1.id, u2.id]:
            user = tmp_db.get_user_by_id(uid)
            assert user.current_phase == 1
            assert user.completed is False

        assert tmp_db.get_accessed_documents(u1.id) == []
