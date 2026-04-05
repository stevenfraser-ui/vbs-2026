"""Shared fixtures for intel-station tests."""

import sqlite3
import sys
import threading
from pathlib import Path
from unittest.mock import MagicMock

import pytest

# ── Module-level streamlit mock ──────────────────────────────────────
# Must be installed BEFORE any test module imports src.services.*,
# otherwise the real @st.cache_resource() decorator wraps init_db and
# caches it, preventing table creation in per-test temp DBs.
_mock_st = MagicMock()
_mock_st.cache_resource.return_value = lambda fn: fn
sys.modules.setdefault("streamlit", _mock_st)


@pytest.fixture()
def tmp_db(tmp_path):
    """Provide an isolated in-memory-like SQLite database for each test.

    Patches database_service to use a temp file DB, initialises the schema,
    and tears down the thread-local connection afterwards.
    """
    from src.services import database_service as db_mod

    db_file = tmp_path / "test.db"

    # Replace the module-level DB_PATH so every helper uses our temp DB
    original_path = db_mod.DB_PATH
    db_mod.DB_PATH = db_file

    # Reset thread-local connection so a fresh one is created
    if hasattr(db_mod._local, "conn"):
        try:
            db_mod._local.conn.close()
        except Exception:
            pass
        del db_mod._local.conn

    # Initialise schema
    db_mod.init_db()

    yield db_mod

    # Cleanup
    if hasattr(db_mod._local, "conn"):
        try:
            db_mod._local.conn.close()
        except Exception:
            pass
        del db_mod._local.conn
    db_mod.DB_PATH = original_path
