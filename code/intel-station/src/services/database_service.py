import sqlite3
import threading
from datetime import datetime
from contextlib import contextmanager

from src.config.settings import DB_PATH
from src.models.user import User
from src.models.chat import ChatMessage
from src.models.asset import UnlockedAsset

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
        raise


def init_db():
    """Create tables if they don't exist."""
    with get_db() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                code TEXT NOT NULL UNIQUE,
                age INTEGER NOT NULL,
                current_phase INTEGER DEFAULT 1,
                current_substep INTEGER DEFAULT 1,
                completed INTEGER DEFAULT 0,
                created_at TEXT DEFAULT (datetime('now')),
                updated_at TEXT DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                message TEXT NOT NULL,
                phase INTEGER NOT NULL,
                substep INTEGER NOT NULL,
                timestamp TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS unlocked_assets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                asset_key TEXT NOT NULL,
                phase INTEGER NOT NULL,
                substep INTEGER NOT NULL,
                unlocked_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS accessed_documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                doc_filename TEXT NOT NULL,
                category TEXT NOT NULL,
                phase INTEGER NOT NULL,
                substep INTEGER NOT NULL,
                accessed_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );

            CREATE INDEX IF NOT EXISTS idx_users_code ON users(code);
            CREATE INDEX IF NOT EXISTS idx_chat_user ON chat_history(user_id);
            CREATE INDEX IF NOT EXISTS idx_assets_user ON unlocked_assets(user_id);
            CREATE INDEX IF NOT EXISTS idx_accessed_docs_user ON accessed_documents(user_id);
            CREATE UNIQUE INDEX IF NOT EXISTS idx_accessed_docs_unique
                ON accessed_documents(user_id, doc_filename);
        """)


# --- User CRUD ---

def _row_to_user(row: sqlite3.Row) -> User:
    return User(
        id=row["id"],
        name=row["name"],
        code=row["code"],
        age=row["age"],
        current_phase=row["current_phase"],
        current_substep=row["current_substep"],
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
        return get_user_by_id(cursor.lastrowid)


def update_user(user_id: int, **kwargs) -> User | None:
    allowed = {"name", "code", "age", "current_phase", "current_substep", "completed"}
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
    return get_user_by_id(user_id)


def delete_user(user_id: int) -> bool:
    with get_db() as conn:
        cursor = conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
        return cursor.rowcount > 0


def reset_user_progress(user_id: int) -> User | None:
    with get_db() as conn:
        conn.execute(
            "UPDATE users SET current_phase=1, current_substep=1, "
            "completed=0, updated_at=datetime('now') WHERE id = ?",
            (user_id,),
        )
        conn.execute(
            "DELETE FROM chat_history WHERE user_id = ?", (user_id,)
        )
        conn.execute(
            "DELETE FROM unlocked_assets WHERE user_id = ?", (user_id,)
        )
        conn.execute(
            "DELETE FROM accessed_documents WHERE user_id = ?", (user_id,)
        )
    return get_user_by_id(user_id)


def reset_all_progress():
    with get_db() as conn:
        conn.execute(
            "UPDATE users SET current_phase=1, current_substep=1, "
            "completed=0, updated_at=datetime('now')"
        )
        conn.execute("DELETE FROM chat_history")
        conn.execute("DELETE FROM unlocked_assets")
        conn.execute("DELETE FROM accessed_documents")


# --- Chat History ---

def add_chat_message(user_id: int, role: str, message: str,
                     phase: int, substep: int) -> ChatMessage:
    with get_db() as conn:
        cursor = conn.execute(
            "INSERT INTO chat_history (user_id, role, message, phase, substep) "
            "VALUES (?, ?, ?, ?, ?)",
            (user_id, role, message, phase, substep),
        )
        row = conn.execute(
            "SELECT * FROM chat_history WHERE id = ?", (cursor.lastrowid,)
        ).fetchone()
        return ChatMessage(
            id=row["id"],
            user_id=row["user_id"],
            role=row["role"],
            message=row["message"],
            phase=row["phase"],
            substep=row["substep"],
            timestamp=datetime.fromisoformat(row["timestamp"]),
        )


def get_chat_history(user_id: int, limit: int = 50) -> list[ChatMessage]:
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM chat_history WHERE user_id = ? "
            "ORDER BY timestamp ASC LIMIT ?",
            (user_id, limit),
        ).fetchall()
        return [
            ChatMessage(
                id=r["id"], user_id=r["user_id"], role=r["role"],
                message=r["message"], phase=r["phase"],
                substep=r["substep"],
                timestamp=datetime.fromisoformat(r["timestamp"]),
            )
            for r in rows
        ]


# --- Unlocked Assets ---

def unlock_asset(user_id: int, asset_key: str,
                 phase: int, substep: int) -> UnlockedAsset:
    with get_db() as conn:
        # Avoid duplicates
        existing = conn.execute(
            "SELECT * FROM unlocked_assets WHERE user_id = ? AND asset_key = ?",
            (user_id, asset_key),
        ).fetchone()
        if existing:
            return UnlockedAsset(
                id=existing["id"], user_id=existing["user_id"],
                asset_key=existing["asset_key"], phase=existing["phase"],
                substep=existing["substep"],
                unlocked_at=datetime.fromisoformat(existing["unlocked_at"]),
            )
        cursor = conn.execute(
            "INSERT INTO unlocked_assets (user_id, asset_key, phase, substep) "
            "VALUES (?, ?, ?, ?)",
            (user_id, asset_key, phase, substep),
        )
        row = conn.execute(
            "SELECT * FROM unlocked_assets WHERE id = ?", (cursor.lastrowid,)
        ).fetchone()
        return UnlockedAsset(
            id=row["id"], user_id=row["user_id"],
            asset_key=row["asset_key"], phase=row["phase"],
            substep=row["substep"],
            unlocked_at=datetime.fromisoformat(row["unlocked_at"]),
        )


def get_unlocked_assets(user_id: int) -> list[UnlockedAsset]:
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM unlocked_assets WHERE user_id = ? "
            "ORDER BY unlocked_at ASC",
            (user_id,),
        ).fetchall()
        return [
            UnlockedAsset(
                id=r["id"], user_id=r["user_id"],
                asset_key=r["asset_key"], phase=r["phase"],
                substep=r["substep"],
                unlocked_at=datetime.fromisoformat(r["unlocked_at"]),
            )
            for r in rows
        ]


# --- Accessed Documents (Knowledge Base) ---

def record_document_access(user_id: int, doc_filename: str, category: str,
                           phase: int, substep: int) -> None:
    """Record that a user has accessed a KB document. Ignores duplicates."""
    with get_db() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO accessed_documents "
            "(user_id, doc_filename, category, phase, substep) "
            "VALUES (?, ?, ?, ?, ?)",
            (user_id, doc_filename, category, phase, substep),
        )


def get_accessed_documents(user_id: int) -> list[dict]:
    """Get all KB documents accessed by a user, ordered by access time."""
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
                "substep": r["substep"],
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
