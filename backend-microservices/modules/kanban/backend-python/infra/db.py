import os
import psycopg2


def get_db_connection():
    """
    Returns a new PostgreSQL connection.
    Uses DATABASE_URL from environment.
    """
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL is not set")

    return psycopg2.connect(database_url)
