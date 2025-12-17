from fastapi import APIRouter
from pydantic import BaseModel
from services.board_service import create_board

router = APIRouter()

class BoardCreate(BaseModel):
    project_id: str
    name: str

@router.post("/boards")
def create(board: BoardCreate):
    return create_board(board.project_id, board.name)


