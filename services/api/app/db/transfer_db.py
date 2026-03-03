from typing import Optional

from . import _get_conn


def record_transfer(user_from: str, user_to: str, amount: str) -> Optional[int]:
    with _get_conn() as conn:
        cursor = conn.execute(
            "INSERT INTO transfers (user_from, user_to, amount) VALUES (?, ?, ?)",
            (user_from, user_to, amount),
        )
        return cursor.lastrowid
