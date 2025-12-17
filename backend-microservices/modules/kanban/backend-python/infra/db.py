import os
import time
import psycopg2
from psycopg2 import OperationalError

DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection(
    retries: int = 10,
    delay: float = 1.5,
):
    last_error = None

    for attempt in range(retries):
        try:
            return psycopg2.connect(DATABASE_URL)
        except OperationalError as e:
            last_error = e
            time.sleep(delay)

    # If we get here, DB never became available
    raise last_error


def ensure_tables(conn):
    with conn.cursor() as cur:
        # Required for UUID generation
        cur.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto;")

        cur.execute("""
        CREATE TABLE IF NOT EXISTS boards (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            project_id UUID NOT NULL,
            name TEXT NOT NULL,
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            CONSTRAINT fk_project
                FOREIGN KEY (project_id)
                REFERENCES projects(id)
                ON DELETE CASCADE
        );
        """)

    conn.commit()
