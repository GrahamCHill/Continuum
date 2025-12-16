import uuid
from datetime import datetime
from domain.board import Board
from infra.db import get_db_connection


def create_board(project_id: str, name: str) -> Board:
    board_id = str(uuid.uuid4())

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO boards (id, project_id, name, created_at)
        VALUES (%s, %s, %s, %s)
        """,
        (board_id, project_id, name, datetime.utcnow()),
    )

    conn.commit()
    cur.close()
    conn.close()

    return Board(
        id=board_id,
        project_id=project_id,
        name=name,
    )
