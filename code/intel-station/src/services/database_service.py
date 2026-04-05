import logging
import sqlite3
import threading
from datetime import datetime
from contextlib import contextmanager

import streamlit as st

from src.config.settings import DB_PATH
from src.models.user import User

logger = logging.getLogger(__name__)

_local = threading.local()


def _get_connection() -> sqlite3.Connection:
    """Get a thread-local database connection with WAL mode."""
    if not hasattr(_local, "conn") or _local.conn is None:
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")
        conn.row_factory = sqlite3.Row
        _local.conn = conn
    return _local.conn


@contextmanager
def get_db():
    """Context manager that yields a DB connection and commits on success."""
    conn = _get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        logger.error("DB transaction rolled back", exc_info=True)
        raise


@st.cache_resource()
def init_db():
    """Create tables if they don't exist."""
    logger.info("Initializing database at %s", DB_PATH)
    with get_db() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                code TEXT NOT NULL UNIQUE,
                age INTEGER NOT NULL,
                current_phase INTEGER DEFAULT 1,
                completed INTEGER DEFAULT 0,
                created_at TEXT DEFAULT (datetime('now')),
                updated_at TEXT DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS accessed_documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                doc_filename TEXT NOT NULL,
                category TEXT NOT NULL,
                phase INTEGER NOT NULL,
                accessed_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );

            CREATE INDEX IF NOT EXISTS idx_users_code ON users(code);
            CREATE INDEX IF NOT EXISTS idx_accessed_docs_user ON accessed_documents(user_id);
            CREATE UNIQUE INDEX IF NOT EXISTS idx_accessed_docs_unique
                ON accessed_documents(user_id, doc_filename);
        """)
    logger.info("Database initialized successfully")


# --- User CRUD ---

def _row_to_user(row: sqlite3.Row) -> User:
    return User(
        id=row["id"],
        name=row["name"],
        code=row["code"],
        age=row["age"],
        current_phase=row["current_phase"],
        completed=bool(row["completed"]),
        created_at=datetime.fromisoformat(row["created_at"]),
        updated_at=datetime.fromisoformat(row["updated_at"]),
    )


def get_user_by_code(code: str) -> User | None:
    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM users WHERE code = ?", (code,)
        ).fetchone()
        return _row_to_user(row) if row else None


def get_user_by_id(user_id: int) -> User | None:
    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM users WHERE id = ?", (user_id,)
        ).fetchone()
        return _row_to_user(row) if row else None


def get_all_users() -> list[User]:
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM users ORDER BY name"
        ).fetchall()
        return [_row_to_user(r) for r in rows]


def create_user(name: str, code: str, age: int) -> User:
    with get_db() as conn:
        cursor = conn.execute(
            "INSERT INTO users (name, code, age) VALUES (?, ?, ?)",
            (name, code, age),
        )
        user = get_user_by_id(cursor.lastrowid)
        logger.info("User created: id=%d name=%r age=%d", user.id, user.name, user.age)
        return user


def update_user(user_id: int, **kwargs) -> User | None:
    allowed = {"name", "code", "age", "current_phase", "completed"}
    fields = {k: v for k, v in kwargs.items() if k in allowed}
    if not fields:
        return get_user_by_id(user_id)
    fields["updated_at"] = datetime.now().isoformat()
    set_clause = ", ".join(f"{k} = ?" for k in fields)
    values = list(fields.values()) + [user_id]
    with get_db() as conn:
        conn.execute(
            f"UPDATE users SET {set_clause} WHERE id = ?", values
        )
    logger.debug("User updated: id=%d fields=%s", user_id, list(fields.keys()))
    return get_user_by_id(user_id)


def delete_user(user_id: int) -> bool:
    with get_db() as conn:
        cursor = conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
        deleted = cursor.rowcount > 0
    if deleted:
        logger.info("User deleted: id=%d", user_id)
    return deleted


def reset_user_progress(user_id: int) -> User | None:
    with get_db() as conn:
        conn.execute(
            "UPDATE users SET current_phase=1, "
            "completed=0, updated_at=datetime('now') WHERE id = ?",
            (user_id,),
        )
        conn.execute(
            "DELETE FROM accessed_documents WHERE user_id = ?", (user_id,)
        )
    logger.info("User progress reset: id=%d", user_id)
    return get_user_by_id(user_id)


def reset_all_progress():
    with get_db() as conn:
        conn.execute(
            "UPDATE users SET current_phase=1, "
            "completed=0, updated_at=datetime('now')"
        )
        conn.execute("DELETE FROM accessed_documents")
    logger.info("All user progress reset")


# --- Accessed Documents ---

def record_document_access(user_id: int, doc_filename: str, category: str,
                           phase: int) -> None:
    """Record that a user has accessed an intel document. Ignores duplicates."""
    with get_db() as conn:
        cursor = conn.execute(
            "INSERT OR IGNORE INTO accessed_documents "
            "(user_id, doc_filename, category, phase) "
            "VALUES (?, ?, ?, ?)",
            (user_id, doc_filename, category, phase),
        )
    if cursor.rowcount:
        logger.info(
            "Document accessed: user_id=%d doc=%r category=%s phase=%d",
            user_id, doc_filename, category, phase,
        )


def get_accessed_documents(user_id: int) -> list[dict]:
    """Get all documents accessed by a user, ordered by access time."""
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM accessed_documents WHERE user_id = ? "
            "ORDER BY accessed_at ASC",
            (user_id,),
        ).fetchall()
        return [
            {
                "id": r["id"],
                "user_id": r["user_id"],
                "doc_filename": r["doc_filename"],
                "category": r["category"],
                "phase": r["phase"],
                "accessed_at": r["accessed_at"],
            }
            for r in rows
        ]


def get_accessed_documents_for_phase(user_id: int, phase: int) -> list[dict]:
    """Get documents accessed by a user for a specific phase."""
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM accessed_documents WHERE user_id = ? AND phase = ? "
            "ORDER BY accessed_at ASC",
            (user_id, phase),
        ).fetchall()
        return [
            {
                "id": r["id"],
                "user_id": r["user_id"],
                "doc_filename": r["doc_filename"],
                "category": r["category"],
                "phase": r["phase"],
                "accessed_at": r["accessed_at"],
            }
            for r in rows
        ]


def get_accessed_doc_filenames(user_id: int) -> list[str]:
    """Get just the filenames of documents a user has accessed."""
    with get_db() as conn:
        rows = conn.execute(
            "SELECT doc_filename FROM accessed_documents WHERE user_id = ? "
            "ORDER BY accessed_at ASC",
            (user_id,),
        ).fetchall()
        return [r["doc_filename"] for r in rows]
