from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import get_db
from services.chat_orchestration import ChatOrchestrationService

router = APIRouter(prefix="/api/chat", tags=["Chat"])

class ChatRequest(BaseModel):
    node_id: str
    content: str

@router.post("/", status_code=status.HTTP_201_CREATED)
def chat_endpoint(payload: ChatRequest, db: Session = Depends(get_db)):
    """
    Receives user chat input and node_id, delegates to the 
    ChatOrchestrationService, and returns the AI's response.
    """
    saved_ai_message = ChatOrchestrationService.process_chat(
        db=db, 
        node_id=payload.node_id, 
        user_content=payload.content
    )

    return {
        "status": "success",
        "user_query": payload.content,
        "ai_response": saved_ai_message.content,
        "ai_message_id": saved_ai_message.id
    }