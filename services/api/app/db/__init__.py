# WARNING
# This is intentionally vulnerable and must never be used in production.
# WARNING
import os
import sqlite3


DB_PATH = os.path.join(os.path.dirname(__file__), "transfers.sqlite3")


def _get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    with _get_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS transfers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_from TEXT NOT NULL,
                user_to TEXT NOT NULL,
                amount TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
            """
        )
        cursor = conn.execute("SELECT COUNT(*) FROM transfers")
        existing = cursor.fetchone()[0]
        if existing == 0:
            conn.executemany(
                "INSERT INTO transfers (user_from, user_to, amount) VALUES (?, ?, ?)",
                [
                    ("user1", "user2", "50"),
                    ("user1", "user2", "100"),
                    ("user1", "user2", "150"),
                    ("user2", "user3", "200"),
                    ("user2", "user3", "300"),
                ],
            )


init_db()
