import os

from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

pool = ConnectionPool(
    os.environ["DATABASE_URL"],
    kwargs={"row_factory": dict_row}
)

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
