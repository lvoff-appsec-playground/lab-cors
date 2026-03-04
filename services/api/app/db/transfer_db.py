from typing import Optional

from . import _get_conn


def record_transfer(user_from: str, user_to: str, amount: str) -> Optional[int]:
    with _get_conn() as conn:
        cursor = conn.execute(
            "INSERT INTO transfers (user_from, user_to, amount) VALUES (?, ?, ?)",
            (user_from, user_to, amount),
        )
        return cursor.lastrowid


def list_transfers_by_user(user_from: str) -> list[dict]:
    with _get_conn() as conn:
        cursor = conn.execute(
            """
            SELECT id, user_from, user_to, amount, created_at
            FROM transfers
            WHERE user_from = ?
            ORDER BY id DESC
            """,
            (user_from,),
        )
        return [
            {
                "id": row[0],
                "user_from": row[1],
                "user_to": row[2],
                "amount": row[3],
                "created_at": row[4],
            }
            for row in cursor.fetchall()
        ]


def latest_transfer_id_by_user(user_from: str) -> Optional[int]:
    with _get_conn() as conn:
        cursor = conn.execute(
            "SELECT id FROM transfers WHERE user_from = ? ORDER BY id DESC LIMIT 1",
            (user_from,),
        )
        row = cursor.fetchone()
        if not row:
            return None
        return row[0]


def list_all_transfers() -> list[dict]:
    with _get_conn() as conn:
        cursor = conn.execute(
            """
            SELECT id, user_from, user_to, amount, created_at
            FROM transfers
            ORDER BY id DESC
            """
        )
        return [
            {
                "id": row[0],
                "user_from": row[1],
                "user_to": row[2],
                "amount": row[3],
                "created_at": row[4],
            }
            for row in cursor.fetchall()
        ]
