from pydantic import BaseModel
from typing import Optional, List

class DiagramCreate(BaseModel):
    title: str
    description: Optional[str] = None
    content: str
    created_by: Optional[str] = None
    tags: Optional[List[str]] = None

class DiagramResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    s3_key: str
    diagram_type: str
    created_at: str
    updated_at: str
    created_by: Optional[str]
    tags: Optional[List[str]]
    content_url: Optional[str] = None
