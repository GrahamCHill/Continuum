def ensure_tables(conn):
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS boards (
            id UUID PRIMARY KEY,
            project_id TEXT NOT NULL,
            name TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT fk_project
                FOREIGN KEY (project_id)
                REFERENCES projects(id)
                ON DELETE CASCADE
        )
        """)
        conn.commit()
