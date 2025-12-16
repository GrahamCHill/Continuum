from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel

from services.chat_service import chat

router = APIRouter()

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    force_local: Optional[bool] = False

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    return chat(request)
