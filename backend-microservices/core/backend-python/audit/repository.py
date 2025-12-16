import psycopg2
import os
import json
from datetime import datetime

DATABASE_URL = os.getenv("DATABASE_URL")
SERVICE_NAME = "backend-python"

def persist_audit_event(
    action: str,
    entity: str = None,
    entity_id: str = None,
    user_id: str = None,
    request_ip: str = None,
    details: dict = None,
):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO audit_log (
            timestamp,
            service,
            user_id,
            action,
            entity,
            entity_id,
            request_ip,
            details
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        datetime.utcnow(),
        SERVICE_NAME,
        user_id,
        action,
        entity,
        entity_id,
        request_ip,
        json.dumps(details) if details else None,
    ))

    conn.commit()
    cur.close()
    conn.close()
