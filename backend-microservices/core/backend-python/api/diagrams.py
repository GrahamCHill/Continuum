from fastapi import APIRouter, HTTPException
from typing import List

from models.diagram_models import DiagramCreate, DiagramResponse
from services.diagram_service import (
    create_diagram,
    list_diagrams,
    get_diagram,
    update_diagram,
    delete_diagram,
    get_diagram_content,
)

router = APIRouter()

@router.post("/diagrams", response_model=DiagramResponse)
def create(diagram: DiagramCreate):
    return create_diagram(diagram)

@router.get("/diagrams", response_model=List[DiagramResponse])
def list_all(limit: int = 50, offset: int = 0):
    return list_diagrams(limit, offset)

@router.get("/diagrams/{diagram_id}", response_model=DiagramResponse)
def get(diagram_id: str):
    return get_diagram(diagram_id)

@router.get("/diagrams/{diagram_id}/content")
def content(diagram_id: str):
    return get_diagram_content(diagram_id)

@router.put("/diagrams/{diagram_id}")
def update(diagram_id: str, diagram: DiagramCreate):
    return update_diagram(diagram_id, diagram)

@router.delete("/diagrams/{diagram_id}")
def delete(diagram_id: str):
    return delete_diagram(diagram_id)
