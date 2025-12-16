import uuid
from fastapi import HTTPException

from infra.db import get_connection
from infra.s3 import (
    upload_diagram,
    download_diagram,
    delete_diagram,
    get_presigned_url,
)
from models.diagram_models import DiagramCreate, DiagramResponse

def create_diagram(diagram: DiagramCreate) -> DiagramResponse:
    s3_key = upload_diagram(diagram.content)

    conn = get_connection()
    cur = conn.cursor()

    diagram_id = str(uuid.uuid4())
    cur.execute("""
        INSERT INTO diagrams (id, title, description, s3_key, created_by, tags)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id, title, description, s3_key, diagram_type,
                  created_at, updated_at, created_by, tags
    """, (
        diagram_id,
        diagram.title,
        diagram.description,
        s3_key,
        diagram.created_by,
        diagram.tags,
    ))

    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    return DiagramResponse(
        id=str(row[0]),
        title=row[1],
        description=row[2],
        s3_key=row[3],
        diagram_type=row[4],
        created_at=row[5].isoformat(),
        updated_at=row[6].isoformat(),
        created_by=row[7],
        tags=row[8],
        content_url=get_presigned_url(s3_key),
    )

def list_diagrams(limit: int, offset: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, title, description, s3_key, diagram_type,
               created_at, updated_at, created_by, tags
        FROM diagrams
        ORDER BY created_at DESC
        LIMIT %s OFFSET %s
    """, (limit, offset))

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        DiagramResponse(
            id=str(r[0]),
            title=r[1],
            description=r[2],
            s3_key=r[3],
            diagram_type=r[4],
            created_at=r[5].isoformat(),
            updated_at=r[6].isoformat(),
            created_by=r[7],
            tags=r[8],
            content_url=get_presigned_url(r[3]),
        )
        for r in rows
    ]

def get_diagram(diagram_id: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, title, description, s3_key, diagram_type,
               created_at, updated_at, created_by, tags
        FROM diagrams WHERE id = %s
    """, (diagram_id,))

    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Diagram not found")

    return DiagramResponse(
        id=str(row[0]),
        title=row[1],
        description=row[2],
        s3_key=row[3],
        diagram_type=row[4],
        created_at=row[5].isoformat(),
        updated_at=row[6].isoformat(),
        created_by=row[7],
        tags=row[8],
        content_url=get_presigned_url(row[3]),
    )

def get_diagram_content(diagram_id: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT s3_key FROM diagrams WHERE id = %s", (diagram_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Diagram not found")

    return {"content": download_diagram(row[0])}

def update_diagram(diagram_id: str, diagram: DiagramCreate):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT s3_key FROM diagrams WHERE id = %s", (diagram_id,))
    row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Diagram not found")

    old_key = row[0]
    new_key = upload_diagram(diagram.content)
    delete_diagram(old_key)

    cur.execute("""
        UPDATE diagrams
        SET title=%s, description=%s, s3_key=%s, tags=%s,
            updated_at=CURRENT_TIMESTAMP
        WHERE id=%s
    """, (
        diagram.title,
        diagram.description,
        new_key,
        diagram.tags,
        diagram_id,
    ))

    conn.commit()
    cur.close()
    conn.close()

    return get_diagram(diagram_id)

def delete_diagram(diagram_id: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT s3_key FROM diagrams WHERE id = %s", (diagram_id,))
    row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Diagram not found")

    delete_diagram(row[0])
    cur.execute("DELETE FROM diagrams WHERE id = %s", (diagram_id,))
    conn.commit()
    cur.close()
    conn.close()

    return {"message": "Diagram deleted successfully"}
