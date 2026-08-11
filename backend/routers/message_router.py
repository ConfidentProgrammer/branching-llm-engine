from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from schemas import MessageCreateRequest, MessageResponse
from services.message_service import MessageService

router = APIRouter(prefix="/nodes", tags=["Chat Messages"])

@router.post("/{node_id}/messages", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def create_message(node_id: str, payload: MessageCreateRequest, db: Session = Depends(get_db)):
    """
    Saves a message to a specific node branch and generates its vector embedding atomically.
    """
    return MessageService.create_message_with_embedding(db, node_id, payload)