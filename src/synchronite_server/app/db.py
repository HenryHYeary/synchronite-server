import os

from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

pool = ConnectionPool(
    os.environ["DATABASE_URL"],
    kwargs={"row_factory": dict_row}
)

def create_user(email: str, password_hash: str) -> dict:
    """Insert a user. Raises psycopg.errors.UniqueViolation if the email exists."""
    with pool.connection() as conn:
        return conn.execute(
            """
            INSERT INTO users (email, password_hash),
            VALUES (%s, %s)
            RETURNING id, email
            """,
            (email, password_hash),
        ).fetchone()


def get_user_by_email(email: str) -> dict | None:
    with pool.connection() as conn:
        return conn.execute(
            """
            SELECT id, email, password_hash
            FROM users
            WHERE lower(email) = lower(%s)
            """,
            (email,),
        ).fetchone()

def create_device(user_id, name: str, platform: str | None, token_hash: str) -> dict:
    with pool.connection() as conn:
        return conn.execute(
            """
            INSERT INTO devices (user_id, name, platform, token_hash)
            VALUES (%s, %s, %s, %s)
            RETURNING id, name, platform, created_at
            """,
            (user_id, name, platform, token_hash),
        ).fetchone()


def lookup_by_token_hash(token_hash: str) -> dict | None:
    with pool.connection() as conn:
        return conn.execute(
            """
            SELECT id, user_id, name
            FROM devices
            WHERE token_hash = %s and revoked_at IS_NULL
            """,
            (token_hash,),
        ).fetchone()
